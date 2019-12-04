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
    """Checks that h2 tags exist, and that at least one h2 contains at least one keyword.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    no_h2 = custom_list.CustomList(
        name=_("No h2 tag"),
        settings=_("at least one"),
        found=pgettext("masculin", "none"),
        description=_(
            "H2 tags are useful because they are explored by search engines and can help them understand the subject of your page."
        ),
    )

    enough_h2 = custom_list.CustomList(
        name=_("H2 tags were found"),
        settings=pgettext("feminin", "at least one"),
        description=no_h2.description,
    )

    no_keywords = custom_list.CustomList(
        name=_("No keyword in h2 tags"),
        settings=pgettext("masculin", "at least one"),
        found=pgettext("masculin", "none"),
        description=_(
            "Google uses h2 tags to better understand the subjects of your page."
        ),
    )

    enough_keywords = custom_list.CustomList(
        name=_("Keyword found in h2 tags"),
        settings=pgettext("masculin", "at least one"),
        found=pgettext("masculin", "none"),
        description=no_keywords.description,
    )

    h2 = site.soup.find_all("h2")
    if not h2:
        site.warnings.append(no_h2)
    else:
        enough_h2.found = len(h2)
        enough_h2.searched_in = [t.text for t in h2]
        site.success.append(enough_h2)

        occurence = []
        # check if each keyword
        for keyword in site.keywords:
            # is present at least
            for single_h2 in h2:
                occurence.append(
                    sum(
                        1
                        for _ in re.finditer(
                            r"\b%s\b" % re.escape(keyword.lower()),
                            single_h2.text.lower(),
                        )
                    )
                )
        # if no keyword is found in h2
        if not any(i > 0 for i in occurence):
            no_keywords.searched_in = [t.text for t in h2]
            site.warnings.append(no_keywords)
        else:
            enough_keywords.searched_in = [t.text for t in h2]
            enough_keywords.found = max(i for i in occurence)
            site.success.append(enough_keywords)
