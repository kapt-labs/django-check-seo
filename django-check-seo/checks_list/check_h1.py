# Standard Library
import re

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

    h1 = site.soup.find_all("h1")

    if len(h1) > 1:
        too_much_h1.found = len(h1)
        too_much_h1.searched_in = [t.text for t in h1]
        site.problems.append(too_much_h1)

    elif not h1:
        not_enough_h1.found = pgettext("masculin", "none")
        site.problems.append(not_enough_h1)

    else:

        right_number_h1.found = len(h1)
        right_number_h1.searched_in = [t.text for t in h1]
        site.success.append(right_number_h1)

        # h1 text can be content of alt tag in img
        if not h1[0].text and h1[0].find("img", {"alt": True}):
            h1_text = h1[0].find("img")["alt"].lower()
        # of it can be the text in h1
        else:
            h1_text = h1[0].text.lower()

        occurence = []
        for keyword in site.keywords:
            occurence.append(
                sum(
                    1
                    for _ in re.finditer(
                        r"\b%s\b" % re.escape(keyword.lower()), h1_text,
                    )
                )
            )
        # if no keyword is found in h1
        if not any(i > 0 for i in occurence):
            no_keywords.found = pgettext("masculin", "none")
            no_keywords.searched_in = [t.text for t in h1]
            site.problems.append(no_keywords)
        else:
            enough_keywords.found = max(i for i in occurence)
            enough_keywords.searched_in = [t.text for t in h1]
            site.success.append(enough_keywords)
