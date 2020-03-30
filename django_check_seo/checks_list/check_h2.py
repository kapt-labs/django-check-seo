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
        found="",
        description=no_keywords.description,
    )

    h2 = site.soup.find_all("h2")
    if not h2:
        site.warnings.append(no_h2)
    else:
        enough_h2.found = len(h2)
        enough_h2.searched_in = [get_h2_text(t) for t in h2]
        site.success.append(enough_h2)

        occurrence = []
        h2_kw = []

        # for each h2...
        for single_h2 in h2:
            single_h2 = get_h2_text(single_h2).lower()
            # check if it contains at least 1 keyword
            for keyword in site.keywords:
                keyword_lower = keyword.lower()
                nb_occurrences = len(
                    re.findall(
                        r"(^| |\n|,|\.|!|\?)"
                        + keyword_lower.lower()
                        + r"($| |\n|,|\.|!|\?)",
                        single_h2,
                    )
                )
                occurrence.append(nb_occurrences)

                # add kw in found
                if nb_occurrences > 0:
                    # and add bold in found keywords
                    single_h2 = single_h2.replace(
                        keyword_lower, '<b class="good">' + keyword_lower + "</b>"
                    )
                    if enough_keywords.found != "":
                        enough_keywords.found += ", "
                    enough_keywords.found += keyword

            h2_kw.append(single_h2)
        # if no keyword is found in h2
        if not any(i > 0 for i in occurrence):
            no_keywords.searched_in = [t.text for t in h2]
            no_keywords.found = pgettext("masculin", "none")
            site.warnings.append(no_keywords)
        else:
            enough_keywords.searched_in = h2_kw
            site.success.append(enough_keywords)


def get_h2_text(h2):
    # h2 text can be content of alt tag in img
    if not h2.text and h2.find("img", {"alt": True}):
        return h2.find("img")["alt"]
    # of it can be the text in h2
    else:
        return h2.text
