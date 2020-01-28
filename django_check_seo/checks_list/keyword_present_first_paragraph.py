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
    """Checks that at least one keyword is included in the first paragraph.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    no_keywords = custom_list.CustomList(
        name=_("No keyword in first paragraph"),
        settings=_("before {settings} words").format(
            settings=site.settings.SEO_SETTINGS["keywords_in_first_words"]
        ),
        found=pgettext("masculin", "none"),
        description=_(
            "The reader will be relieved to find one of his keywords in the first paragraph of your page, and the same logic applies to Google, which will consider the content more relevant."
        ),
    )

    found = False
    first_N_words = site.content_text.lower().split()[
        : site.settings.SEO_SETTINGS["keywords_in_first_words"]
    ]
    # check text and not list of words in order that keywords like "this is a keyword" are found in text "words this is a keyword words"
    first_N_words = " ".join(first_N_words)

    nb = 0
    kw = []
    for keyword in site.keywords:
        if keyword.lower() in first_N_words:
            found = True
            kw.append(keyword)
        nb += 1

    no_keywords.searched_in = [first_N_words]

    # no keyword was found in first paragraph
    if not found:
        site.problems.append(no_keywords)

    else:
        no_keywords.name = _("Keywords found in first paragraph")
        no_keywords.found = ", ".join(kw)
        site.success.append(no_keywords)
