# Third party
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy

# Local application / specific library imports
from ..checks import custom_list, utils


def importance():
    """Scripts with higher importance will be executed first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Verifies that only one h1 tag is present, and that it contains at least one keyword.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """
    too_much_h1 = custom_list.CustomList(
        name=_("Too much h1 tags"),
        settings=_("exactly 1"),
        description=_(
            "Google is not really concerned about the number of h1 tags on your page, but Bing clearly indicates in its guidelines for webmasters to use only one h1 tag per page."
        ),
    )

    right_number_h1 = custom_list.CustomList(
        name=_("H1 tag found"),
        settings=_("exactly 1"),
        description=too_much_h1.description,
    )

    not_enough_h1 = custom_list.CustomList(
        name=_("No h1 tag"),
        settings=_("exactly 1"),
        description=too_much_h1.description,
    )

    no_keywords = custom_list.CustomList(
        name=_("No keyword in h1"),
        settings=_("at least one"),
        description=_(
            "The h1 tag represent the main title of your page, and you may populate it with appropriate content in order to ensure that users (and search engines!) will understand correctly your page."
        ),
    )

    enough_keywords = custom_list.CustomList(
        name=_("Keyword found in h1"),
        settings=_("at least one"),
        description=no_keywords.description,
    )

    h1_all = site.soup.find_all("h1")

    if len(h1_all) > 1:
        too_much_h1.found = len(h1_all)
        too_much_h1.searched_in = [utils.get_heading_text(t) for t in h1_all]
        site.problems.append(too_much_h1)

    elif not h1_all:
        not_enough_h1.found = pgettext_lazy("masculin", "none")
        site.problems.append(not_enough_h1)

    else:
        right_number_h1.found = len(h1_all)
        right_number_h1.searched_in = [utils.get_heading_text(t) for t in h1_all]
        site.success.append(right_number_h1)

    enough_keywords.found = ""
    h1_text_kw = []
    occurrence = []
    for h1 in h1_all:
        text = utils.get_heading_text(h1).lower()

        highlighted, occ, found = utils.highlight_keywords_in_text(
            text, site.keywords, normalize_apostrophes_flag=True
        )
        occurrence.extend(occ)
        h1_text_kw.append(highlighted)
        if found:
            enough_keywords.found += (", " if enough_keywords.found else "") + found

    # if no keyword is found in h1
    if not any(i > 0 for i in occurrence):
        no_keywords.found = pgettext_lazy("masculin", "none")
        no_keywords.searched_in = [t.text for t in h1_all]
        site.problems.append(no_keywords)
    else:
        enough_keywords.searched_in = h1_text_kw
        site.success.append(enough_keywords)
