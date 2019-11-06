# Third party
from django.utils.translation import gettext as _


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Check all title-related conditions.
    """
    # title presence
    if site.soup.title == "None":
        site.problems.append(
            {
                "name": _("No title tag"),
                "settings": _("at least 1"),
                "description": _(
                    "Titles tags are ones of the most important things to add to your pages, sinces they are the main text displayed on result search pages."
                ),
            }
        )
        return

    # title length too short
    if len(site.soup.title.string) < site.settings.SEO_SETTINGS["meta_title_length"][0]:
        site.problems.append(
            {
                "name": _("Title tag is too short"),
                "settings": "&ge;{}".format(
                    site.settings.SEO_SETTINGS["meta_title_length"][0]
                ),
                "description": _(
                    "Titles tags need to describe the content of the page, and need to contain at least a few words."
                ),
            }
        )

    # title length too long
    if len(site.soup.title.string) > site.settings.SEO_SETTINGS["meta_title_length"][1]:
        site.warnings.append(
            {
                "name": _("Title tag is too long"),
                "settings": "&le;{}".format(
                    site.settings.SEO_SETTINGS["meta_title_length"][1]
                ),
                "description": _(
                    "Only the first ~55-60 chars are displayed on modern search engines results. Writing a longer title is not really required and can lead to make the user miss informations."
                ),
            }
        )

    title_words = site.soup.title.string.split()

    # title do not contain any keyword
    if set(site.keywords).isdisjoint(set(title_words)):
        site.problems.append(
            {
                "name": _("Title do not contain any keyword"),
                "settings": _("at least 1"),
                "description": _(
                    "Titles tags need to contain at least one keyword, since they are one of the most important content of the page for search engines."
                ),
            }
        )
