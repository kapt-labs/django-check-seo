# Third party
import bs4
from django.contrib.sites.models import Site
from django.utils.translation import gettext as _

# Local application / specific library imports
from ..checks import custom_list


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Counts the number of internal and external links in the extracted content.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    not_enough_internal = custom_list.CustomList(
        name=_("Not enough internal links"),
        settings=_("at least {}").format(
            site.settings.DJANGO_CHECK_SEO_SETTINGS["internal_links"]
        ),
        description=_(
            "Internal links are useful because they can give the structure of your website to search engines, so they can create a hierarchy of your pages."
        ),
    )

    enough_internal = custom_list.CustomList(
        name=_("Internal links were found"),
        settings=_("at least {}").format(
            site.settings.DJANGO_CHECK_SEO_SETTINGS["internal_links"]
        ),
        description=not_enough_internal.description,
    )

    not_enough_external = custom_list.CustomList(
        name=_("Not enough external links"),
        settings=_("at least {}").format(
            site.settings.DJANGO_CHECK_SEO_SETTINGS["external_links"]
        ),
        description=_(
            "External links help your users to check your topic and can save them from having to do additional research."
        ),
    )

    enough_external = custom_list.CustomList(
        name=_("External links were found"),
        settings=_("at least {}").format(
            site.settings.DJANGO_CHECK_SEO_SETTINGS["external_links"]
        ),
        description=not_enough_external.description,
    )

    links = bs4.element.ResultSet(None)

    # only get links with href
    for c in site.content:
        links += c.find_all("a", href=True)

    internal_links = 0
    internal_links_list = []
    external_links_list = []
    external_links = 0

    for link in links:
        # specify if there is text of no text
        if link.text.strip() != "":
            text = link.text
        else:
            childs = link.find_all()
            if len(childs) > 0:
                if childs[0].get("alt", False):
                    text = childs[0]["alt"] + " (&lt;" + childs[0].name + "&gt;)"
                else:
                    text = str(childs[0]).replace("<", "&lt;").replace(">", "&gt;")
            else:
                text = _("[no content]")
        # internal links = absolute links that contains domain name or relative links
        if Site.objects.get_current().domain in link["href"] or not link[
            "href"
        ].startswith("http"):
            internal_links += 1
            internal_links_list.append(
                '<a href="' + link["href"] + '">' + text + "</a>"
            )
        else:
            external_links += 1
            external_links_list.append(
                '<a href="' + link["href"] + '">' + text + "</a>"
            )

    # not enough internal links
    if internal_links < site.settings.DJANGO_CHECK_SEO_SETTINGS["internal_links"]:
        not_enough_internal.found = internal_links
        not_enough_internal.searched_in = internal_links_list
        site.warnings.append(not_enough_internal)
    else:
        enough_internal.found = internal_links
        enough_internal.searched_in = internal_links_list
        site.success.append(enough_internal)

    # not enough external links
    if external_links < site.settings.DJANGO_CHECK_SEO_SETTINGS["external_links"]:
        not_enough_external.found = external_links
        not_enough_external.searched_in = external_links_list
        site.warnings.append(not_enough_external)
    else:
        enough_external.found = external_links
        enough_external.searched_in = external_links_list
        site.success.append(enough_external)
