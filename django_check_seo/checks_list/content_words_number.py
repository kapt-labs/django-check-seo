# Third party
from django.utils.translation import gettext as _

# Local application / specific library imports
from ..checks import custom_list


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Checks the number of words in the extracted content.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    short_content = custom_list.CustomList(
        name=_("Content is too short"),
        settings=_("at least {min} words, more than {min2} if possible").format(
            min=site.settings.DJANGO_CHECK_SEO_SETTINGS["content_words_number"][0],
            min2=site.settings.DJANGO_CHECK_SEO_SETTINGS["content_words_number"][1],
        ),
        description=_(
            "Longer articles tend to be better ranked, but will require better writing skills than shorter articles."
        ),
    )

    nb_words = len(site.content_text.split())
    short_content.found = nb_words
    short_content.searched_in = [site.content_text]

    # too few words
    if nb_words < site.settings.DJANGO_CHECK_SEO_SETTINGS["content_words_number"][0]:
        site.problems.append(short_content)

    elif nb_words < site.settings.DJANGO_CHECK_SEO_SETTINGS["content_words_number"][1]:
        site.warnings.append(short_content)

    else:
        short_content.name = _("Content length is right")
        short_content.searched_in = [
            " ".join(
                site.content_text.split()[
                    : site.settings.DJANGO_CHECK_SEO_SETTINGS["content_words_number"][1]
                ]
            )
            + '<span class="good">'
            + " ".join(
                site.content_text.split()[
                    site.settings.DJANGO_CHECK_SEO_SETTINGS["content_words_number"][1] :
                ]
            )
            + "</span>"
        ]
        site.success.append(short_content)
