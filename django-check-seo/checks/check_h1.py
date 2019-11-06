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

    h1 = site.soup.find_all("h1")
    if len(h1) > 1:
        site.problems.append(
            {
                "name": _("Too much h1 tags"),
                "settings": _("exactly 1"),
                "description": _(
                    'Google has told that they do not consider using multiple h1 a bad thing (<a href="https://www.youtube.com/watch?v=WsgrSxCmMbM">source</a>), but Google is not the unique search engine out there. Bing webmaster guidelines says "Use only one <h1> tag per page".'
                ),
            }
        )

    elif not h1:
        site.problems.append(
            {
                "name": _("No h1 tag"),
                "settings": _("exactly 1"),
                "description": _(
                    "H1 is the most visually notable content of your page for your users, and is one of the most important ranking factor for search engines. A good h1 tag content is required in order to progress in SERP."
                ),
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
                    "name": _("No keyword in h1"),
                    "settings": _("at least 1"),
                    "description": _(
                        "H1 are crawled by search engines as the title of your page. You may populate them with appropriate content in order to be sure that search engines correctly understand what your pages are all about."
                    ),
                }
            )
