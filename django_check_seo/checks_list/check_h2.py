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
    """Checks that h2 tags exist, and that at least one h2 contains at least one keyword.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    no_h2 = custom_list.CustomList(
        name=_("No h2 tag"),
        settings=_("at least one"),
        found=pgettext_lazy("masculin", "none"),
        description=_(
            "H2 tags are useful because they are explored by search engines and can help them understand the subject of your page."
        ),
    )

    enough_h2 = custom_list.CustomList(
        name=_("H2 tags were found"),
        settings=pgettext_lazy("feminin", "at least one"),
        description=no_h2.description,
    )

    no_keywords = custom_list.CustomList(
        name=_("No keyword in h2 tags"),
        settings=pgettext_lazy("masculin", "at least one"),
        found=pgettext_lazy("masculin", "none"),
        description=_(
            "Google uses h2 tags to better understand the subjects of your page."
        ),
    )

    enough_keywords = custom_list.CustomList(
        name=_("Keyword found in h2 tags"),
        settings=pgettext_lazy("masculin", "at least one"),
        found="",
        description=no_keywords.description,
    )

    h2 = site.soup.find_all("h2")
    if not h2:
        site.warnings.append(no_h2)
    else:
        enough_h2.found = len(h2)
        enough_h2.searched_in = [utils.get_heading_text(t) for t in h2]
        site.success.append(enough_h2)

        occurrence = []
        h2_kw = []

        # for each h2...
        for single_h2_tag in h2:
            text = utils.get_heading_text(single_h2_tag).lower()
            highlighted, occ, found = utils.highlight_keywords_in_text(
                text, site.keywords, normalize_apostrophes_flag=True
            )
            occurrence.extend(occ)
            h2_kw.append(highlighted)
            if found:
                enough_keywords.found += (", " if enough_keywords.found else "") + found

        # if no keyword is found in h2
        if not any(i > 0 for i in occurrence):
            no_keywords.searched_in = [t.text for t in h2]
            no_keywords.found = pgettext_lazy("masculin", "none")
            site.warnings.append(no_keywords)
        else:
            enough_keywords.searched_in = h2_kw
            site.success.append(enough_keywords)
