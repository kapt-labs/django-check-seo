# Third party
from django.utils.translation import gettext as _


def keyword_present_first_paragraph(site):
    """Get [keywords_in_first_words] first words of the content, and ensure that there is a keyword among them.
    """
    content = site.content.text.lower().split()[
        : site.settings.SEO_SETTINGS["keywords_in_first_words"]
    ]

    for keyword in site.keywords:
        if keyword in content:
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
