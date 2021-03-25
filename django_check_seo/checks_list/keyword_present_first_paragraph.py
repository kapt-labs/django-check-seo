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
    """Checks that at least one keyword is included in the first paragraph.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    no_keywords = custom_list.CustomList(
        name=_("No keyword in first paragraph"),
        settings=_("before {settings} words").format(
            settings=site.settings.DJANGO_CHECK_SEO_SETTINGS["keywords_in_first_words"]
        ),
        found="",
        description=_(
            "The reader will be relieved to find one of his keywords in the first paragraph of your page, and the same logic applies to Google, which will consider the content more relevant."
        ),
    )

    first_words = site.content_text.lower().split()[
        : site.settings.DJANGO_CHECK_SEO_SETTINGS["keywords_in_first_words"]
    ]
    # check text and not list of words in order to find keywords that looks like "this is a keyword" in text "words this is a keyword words"
    first_words = " ".join(first_words)
    first_words_text = first_words.lower()

    occurrence = []
    first_words_kw = []

    for keyword in site.keywords:
        keyword = keyword.lower()
        nb_occurrences = len(
            re.findall(
                r"(^| |\n|,|\.|!|\?)" + keyword + r"($| |\n|,|\.|!|\?)",
                first_words,
            )
        )
        occurrence.append(nb_occurrences)

        if nb_occurrences > 0:
            first_words_text = first_words_text.replace(
                keyword, '<b class="good">' + keyword + "</b>"
            )
            if no_keywords.found != "":
                no_keywords.found += ", "
            no_keywords.found += keyword
    first_words_kw.append(first_words_text)

    no_keywords.searched_in = first_words_kw

    # no keyword was found in first paragraph
    if not any(i > 0 for i in occurrence):
        no_keywords.found = pgettext("masculin", "none")
        site.problems.append(no_keywords)

    else:
        no_keywords.name = _("Keywords found in first paragraph")
        site.success.append(no_keywords)
