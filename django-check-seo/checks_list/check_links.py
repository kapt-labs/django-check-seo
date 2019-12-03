# Standard Library
import os

# Third party
import bs4
from django.utils.translation import gettext as _, pgettext
import requests

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
        settings=_("at least {}").format(site.settings.SEO_SETTINGS["internal_links"]),
        description=_(
            "Internal links are useful because they can give the structure of your website to search engines, so they can create a hierarchy of your pages."
        ),
    )

    enough_internal = custom_list.CustomList(
        name=_("Internal links were found"),
        settings=_("at least {}").format(site.settings.SEO_SETTINGS["internal_links"]),
        description=not_enough_internal.description,
    )

    broken_internal = custom_list.CustomList(
        name=_("Found broken internal links"),
        settings=pgettext("masculin", "none"),
        description=_(
            "Neither Google nor users like broken links. Consider setting up redirections rather than deleting content on your site."
        ),
    )

    working_internal = custom_list.CustomList(
        name=_("No broken internal link found"),
        settings=pgettext("masculin", "none"),
        found=pgettext("masculin", "none"),
        description=broken_internal.description,
    )

    not_enough_external = custom_list.CustomList(
        name=_("Not enough external links"),
        settings=_("at least {}").format(site.settings.SEO_SETTINGS["external_links"]),
        description=_(
            "External links help your users to check your topic and can save them from having to do additional research."
        ),
    )

    enough_external = custom_list.CustomList(
        name=_("External links were found"),
        settings=_("at least {}").format(site.settings.SEO_SETTINGS["external_links"]),
        description=not_enough_external.description,
    )

    links = bs4.element.ResultSet(None)

    # only get links with href
    for c in site.content:
        links += c.find_all("a", href=True)

    internal_links = 0
    internal_links_list = []
    external_links = 0

    for link in links:
        # internal links = absolute links that contains domain name or relative links
        if os.environ["DOMAIN_NAME"] in link["href"] or not link["href"].startswith(
            "http"
        ):
            internal_links += 1
            internal_links_list.append(link)
        else:
            external_links += 1

    # not enough internal links
    if internal_links < site.settings.SEO_SETTINGS["internal_links"]:
        not_enough_internal.found = internal_links
        site.warnings.append(not_enough_internal)
    else:
        enough_internal.found = internal_links
        site.success.append(enough_internal)

    # not enough external links
    if external_links < site.settings.SEO_SETTINGS["external_links"]:
        not_enough_external.found = external_links
        site.warnings.append(not_enough_external)
    else:
        enough_external.found = external_links
        site.success.append(enough_external)

    # prevent using domain name for loading internal links when testing another website's page
    if os.environ["DOMAIN_NAME"] not in site.full_url:
        domain = site.full_url
        if site.full_url.endswith("/"):
            domain = domain[:-1]
    else:
        domain = "http://" + os.environ["DOMAIN_NAME"]

    # broken internal links
    broken_links = []
    link_text = _("link")
    for link in internal_links_list:

        # prevent bugs if link is absolute and not relative
        if link["href"].startswith("/"):
            link["href"] = domain + link["href"]

        r = requests.get(link["href"]).status_code

        # status is not success or redirect
        if r != 200 and r != 301 and r != 302:
            broken_links.append(
                '<a target="_blank" title="broken link" href="'
                + link["href"]
                + '">'
                + link_text
                + "</a>"
            )

    if len(broken_links) > 0:
        broken_internal.found = str(len(broken_links)) + " - " + ", ".join(broken_links)
        site.problems.append(broken_internal)

    else:
        site.success.append(working_internal)
