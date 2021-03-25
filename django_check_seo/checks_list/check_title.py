# Standard Library
import re

# Third party
from django.utils.translation import gettext as _
from django.utils.translation import pgettext

# Local application / specific library imports
from ..checks import custom_list


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Checks that only one title tag is present, that its content is within a certain range, and that it contains at least one keyword.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    no_title = custom_list.CustomList(
        name=_("No meta title tag"),
        settings=pgettext("feminin", "one"),
        found=_("none"),
        description=_(
            "Titles tags are ones of the most important things to add to your pages, sinces they are the main text displayed on result search pages."
        ),
    )

    too_much = custom_list.CustomList(
        name=_("Too much meta title tags"),
        settings=pgettext("feminin", "only one"),
        description=_(
            "Only the first meta title tag will be displayed on the tab space on your browser, and only one meta title tag will be displayed on the search results pages."
        ),
    )

    short_title = custom_list.CustomList(
        name=_("Meta title tag is too short"),
        settings=_("more than {}").format(
            site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_title_length"][0]
        ),
        description=_(
            "Meta titles tags need to describe the content of the page, and need to contain at least a few words."
        ),
    )

    title_okay = custom_list.CustomList(
        name=_("Meta title tag have a good length"),
        settings=_("more than {}").format(
            site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_title_length"][0]
        ),
        description=_("Meta titles tags need to describe the content of the page."),
    )

    long_title = custom_list.CustomList(
        name=_("Meta title tag is too long"),
        settings=_("less than {}").format(
            site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_title_length"][1]
        ),
        description=_(
            "Only the first ~55-60 chars are displayed on modern search engines results. Writing a longer meta title is not really required and can lead to make the user miss informations."
        ),
    )

    no_keyword = custom_list.CustomList(
        name=_("Meta title tag do not contain any keyword"),
        settings=_("at least one"),
        found=_("none"),
        description=_(
            "Meta titles tags need to contain at least one keyword, since they are one of the most important content of the page for search engines."
        ),
    )

    keyword = custom_list.CustomList(
        name=_("Keywords found in meta title tag"),
        settings=_("at least one"),
        description=no_keyword.description,
    )

    # title presence
    titles = site.soup.head.find_all("title")
    if len(titles) < 1 or titles[0] is None or titles == "None":
        site.problems.append(no_title)
        return

    # multiple titles
    elif titles and len(titles) > 1:
        too_much.found = len(titles)
        too_much.searched_in = [t.string for t in titles]
        site.problems.append(too_much)

    # title length too short
    if (
        len(titles[0].text)
        < site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_title_length"][0]
    ):
        short_title.found = len(titles[0].text)
        short_title.searched_in = [
            titles[0].text if len(titles[0].text) > 0 else _("[no content]")
        ]
        site.problems.append(short_title)

    # title length too long
    elif (
        len(titles[0].string)
        > site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_title_length"][1]
    ):
        long_title.found = len(titles[0].text)
        long_title.searched_in = [
            titles[0].text[
                : site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_title_length"][1]
            ]
            + '<b class="problem">'
            + titles[0].text[
                site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_title_length"][1] :
            ]
            + "</b>"
        ]
        site.warnings.append(long_title)
    else:
        title_okay.found = len(titles[0].text)
        title_okay.searched_in = [
            titles[0].string[
                : site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_title_length"][0]
            ]
            + '<b class="good">'
            + titles[0].string[
                site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_title_length"][0] :
            ]
            + "</b>"
        ]
        site.success.append(title_okay)

    keyword.found = ""
    occurrence = []
    title_text = titles[0].text.lower()
    title_text_kw = []

    for kw in site.keywords:
        kw = kw.lower()
        nb_occurrences = len(
            re.findall(
                r"(^| |\n|,|\.|!|\?)" + kw + r"($| |\n|,|\.|!|\?)",
                title_text,
            )
        )
        occurrence.append(nb_occurrences)

        if nb_occurrences > 0:
            title_text = title_text.replace(
                kw, '<b class="good">' + kw.lower() + "</b>"
            )
            if keyword.found != "":
                keyword.found += ", "
            keyword.found += kw
    title_text_kw.append(title_text)

    # title do not contain any keyword
    if keyword.found == "":
        no_keyword.searched_in = title_text_kw
        site.problems.append(no_keyword)
    else:
        keyword.searched_in = title_text_kw
        site.success.append(keyword)
