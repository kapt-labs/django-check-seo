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
    """Check all h1-related conditions
    """
    too_much_h1 = custom_list.CustomList(
        name=_("Too much h1 tags"),
        settings=_("exactly 1"),
        description=_(
            "Google is not really concerned about the number of h1 tags on your page, but Bing clearly indicates in its guidelines for webmasters to use only one h1 tag per page."
        ),
    )

    right_number_h1 = too_much_h1
    right_number_h1.name = _("H1 tag found")

    not_enough_h1 = too_much_h1
    not_enough_h1.name = _("No h1 tag")

    no_keywords = custom_list.CustomList(
        name=_("No keyword in h1"),
        settings=_("at least one"),
        description=_(
            "The H1 tag represent the main title of your page, and you may populate it with appropriate content in order to ensure that users (and search engines!) will understand correctly your page."
        ),
    )

    enough_keywords = custom_list.CustomList(
        name=_("Keyword found in H1"),
        settings=_("at least one"),
        description=no_keywords.description,
    )

    h1 = site.soup.find_all("h1")
    if len(h1) > 1:
        too_much_h1.found = len(h1)
        site.problems.append(too_much_h1)

    elif not h1:
        too_much_h1.found = pgettext("masculin", "none")
        site.problems.append(not_enough_h1)

    else:

        right_number_h1.found = len(h1)
        site.success.append(right_number_h1)

        occurence = []
        for keyword in site.keywords:
            for single_h1 in h1:
                occurence.append(
                    sum(
                        1
                        for _ in re.finditer(
                            r"\b%s\b" % re.escape(keyword.lower()),
                            single_h1.text.lower(),
                        )
                    )
                )
        # if no keyword is found in h1
        if not any(i > 0 for i in occurence):
            no_keywords.found = _("none")
            site.problems.append(no_keywords)
        else:
            enough_keywords.found = max(i for i in occurence)
            site.success.append(enough_keywords)
