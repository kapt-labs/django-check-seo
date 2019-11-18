# Third party
from django.utils.translation import gettext as _


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Get [keywords_in_first_words] first words of the content, and ensure that there is a keyword among them.
    """
    keywords_name = _("No keyword in first sentence")
    keywords_settings = _(
        "before {settings} words".format(
            settings=site.settings.SEO_SETTINGS["keywords_in_first_words"]
        )
    )
    keywords_found = _("none")
    keywords_description = _(
        "The reader will be relieved to find one of his keywords in the first paragraph of your page, and the same logic applies to Google."
    )

    first_N_words = site.content_text.split()[
        : site.settings.SEO_SETTINGS["keywords_in_first_words"]
    ]

    nb = 0
    for keyword in site.keywords:
        if keyword in first_N_words:
            return
        elif keyword:
            keywords_found = nb
            break
        nb += 1

    site.problems.append(
        {
            "name": keywords_name,
            "settings": keywords_settings,
            "found": keywords_found,
            "description": keywords_description,
        }
    )
