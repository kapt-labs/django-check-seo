# Third party
from django.utils.translation import gettext as _


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Count number of words in content.
    """
    short_content_name = _("Content is too short")
    short_content_settings = _(
        "at least {min} words, more than {min2} if possible"
    ).format(
        min=site.settings.SEO_SETTINGS["content_words_number"][0],
        min2=site.settings.SEO_SETTINGS["content_words_number"][1],
    )
    short_content_description = _(
        "Longer posts tend to be more highly ranked, but will require better writing skills than shorter articles."
    )

    nb_words = len(site.content_text.split())

    # too few words
    if nb_words < site.settings.SEO_SETTINGS["content_words_number"][0]:
        site.problems.append(
            {
                "name": short_content_name,
                "settings": short_content_settings,
                "found": nb_words,
                "description": short_content_description,
            }
        )

    elif nb_words < site.settings.SEO_SETTINGS["content_words_number"][1]:
        site.warnings.append(
            {
                "name": short_content_name,
                "settings": short_content_settings,
                "found": nb_words,
                "description": short_content_description,
            }
        )
