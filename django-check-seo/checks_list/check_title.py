# Third party
from django.utils.translation import gettext as _, pgettext

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
        name=_("No title tag"),
        settings=pgettext("masculin", "one"),
        found=_("none"),
        description=_(
            "Titles tags are ones of the most important things to add to your pages, sinces they are the main text displayed on result search pages."
        ),
    )

    title_found = custom_list.CustomList(
        name=_("Found title tag"),
        settings=pgettext("masculin", "one"),
        found=pgettext("masculin", "one"),
        description=no_title.description,
    )

    too_much = custom_list.CustomList(
        name=_("Too much title tags"),
        settings=pgettext("masculin", "only one"),
        description=_(
            "Only the first title tag will be displayed on the tab space on your browser, and only one title tag will be displayed on the search results pages."
        ),
    )

    short_title = custom_list.CustomList(
        name=_("Title tag is too short"),
        settings=_("more than {}").format(
            site.settings.SEO_SETTINGS["meta_title_length"][0]
        ),
        description=_(
            "Titles tags need to describe the content of the page, and need to contain at least a few words."
        ),
    )

    title_okay = custom_list.CustomList(
        name=_("Title tag have a good length"),
        settings=_("more than {}").format(
            site.settings.SEO_SETTINGS["meta_title_length"][0]
        ),
        description=_("Titles tags need to describe the content of the page."),
    )

    long_title = custom_list.CustomList(
        name=_("Title tag is too long"),
        settings=_(
            "less than {}".format(site.settings.SEO_SETTINGS["meta_title_length"][1])
        ),
        description=_(
            "Only the first ~55-60 chars are displayed on modern search engines results. Writing a longer title is not really required and can lead to make the user miss informations."
        ),
    )

    no_keyword = custom_list.CustomList(
        name=_("Title do not contain any keyword"),
        settings=_("at least one"),
        found=_("none"),
        description=_(
            "Titles tags need to contain at least one keyword, since they are one of the most important content of the page for search engines."
        ),
    )

    keyword = custom_list.CustomList(
        name=_("Keywords found in title"),
        settings=_("at least one"),
        description=no_keyword.description,
    )

    # title presence
    if site.soup.title == "None" or not site.soup.title or not site.soup.title.string:
        site.problems.append(no_title)
        return

    # multiple titles
    elif site.soup.find_all("title") and len(site.soup.find_all("title")) > 1:
        too_much.found = len(site.soup.find_all("title"))
        site.problems.append(too_much)

    site.success.append(title_found)

    # title length too short
    if len(site.soup.title.string) < site.settings.SEO_SETTINGS["meta_title_length"][0]:
        short_title.found = len(site.soup.title.string)
        site.problems.append(short_title)

    # title length too long
    elif (
        len(site.soup.title.string) > site.settings.SEO_SETTINGS["meta_title_length"][1]
    ):
        long_title.found = len(site.soup.title.string)
        site.warnings.append(long_title)
    else:
        title_okay.found = len(site.soup.title.string)
        site.success.append(title_okay)

    keyword.found = ""
    keyword_found = False
    title_readable = site.soup.title.string.lower()

    for kw in site.keywords:
        print(kw)
        if kw.lower() in title_readable:
            if keyword_found:
                keyword.found += ", "
            keyword_found = True
            keyword.found += kw

    # title do not contain any keyword
    if keyword.found == "":
        site.problems.append(no_keyword)
    else:
        site.success.append(keyword)
