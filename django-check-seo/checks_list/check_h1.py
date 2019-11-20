# Standard Library
import re

# Third party
from django.utils.translation import gettext as _


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Check all h1-related conditions
    """
    too_much_name = _("Too much h1 tags")
    too_much_settings = _("exactly 1")
    too_much_description = _(
        "Google is not really concerned about the number of h1 tags on your page, but Bing clearly indicates in its guidelines for webmasters to use only one h1 tag per page."
    )

    too_few_name = _("No h1 tag")
    too_few_settings = _("exactly 1")
    too_few_description = "H1 tag is the most visually notable content of your page for your users, and will help Search Engines to better understand the subject of your page."

    keywords_name = _("No keyword in h1")
    keywords_settings = _("at least 1")
    keywords_description = _(
        "The H1 tag represent the main title of your page, and you may populate it with appropriate content in order to ensure that users (and search engines!) will understand correctly your page."
    )

    h1 = site.soup.find_all("h1")
    if len(h1) > 1:
        site.problems.append(
            {
                "name": too_much_name,
                "settings": too_much_settings,
                "found": len(h1),
                "description": too_much_description,
            }
        )

    elif not h1:
        site.problems.append(
            {
                "name": too_few_name,
                "settings": too_few_settings,
                "found": _("none"),
                "description": too_few_description,
            }
        )

    else:
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
            site.problems.append(
                {
                    "name": keywords_name,
                    "settings": keywords_settings,
                    "found": _("none"),
                    "description": keywords_description,
                }
            )
