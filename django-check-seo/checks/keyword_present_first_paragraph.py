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
    first_N_words = site.content_text.split()[
        : site.settings.SEO_SETTINGS["keywords_in_first_words"]
    ]

    for keyword in site.keywords:
        if keyword in first_N_words:
            return

    site.problems.append(
        {
            "name": _("No keyword in first sentence"),
            "settings": "before {settings} words".format(
                settings=site.settings.SEO_SETTINGS["keywords_in_first_words"]
            ),
            "description": _(
                'Yoast advises to put a keyword in the first sentence of your content. The person who reads it will be relieved because he will quickly retrieve the keyword he was looking for (<a href="https://yoast.com/text-structure-important-seo/">source</a>).'
            ),
        }
    )