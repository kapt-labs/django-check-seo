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

    no_title_name = _("No title tag")
    no_title_settings = _("at least 1")
    no_title_found = _("none")
    no_title_description = _(
        "Titles tags are ones of the most important things to add to your pages, sinces they are the main text displayed on result search pages."
    )

    short_title_name = _("Title tag is too short")
    short_title_settings = _("longer than {}").format(
        site.settings.SEO_SETTINGS["meta_title_length"][0]
    )
    short_title_description = _(
        "Titles tags need to describe the content of the page, and need to contain at least a few words."
    )

    long_title_name = _("Title tag is too long")
    long_title_settings = _(
        "less than {}".format(site.settings.SEO_SETTINGS["meta_title_length"][1])
    )
    long_title_description = _(
        "Only the first ~55-60 chars are displayed on modern search engines results. Writing a longer title is not really required and can lead to make the user miss informations."
    )

    keyword_title_name = _("Title do not contain any keyword")
    keyword_title_settings = _("at least 1")
    keyword_title_found = "none"
    keyword_title_description = _(
        "Titles tags need to contain at least one keyword, since they are one of the most important content of the page for search engines."
    )

    # title presence
    if site.soup.title == "None":
        site.problems.append(
            {
                "name": no_title_name,
                "settings": no_title_settings,
                "found": no_title_found,
                "description": no_title_description,
            }
        )
        return

    # title length too short
    if len(site.soup.title.string) < site.settings.SEO_SETTINGS["meta_title_length"][0]:
        site.problems.append(
            {
                "name": short_title_name,
                "settings": short_title_settings,
                "found": len(site.soup.title.string),
                "description": short_title_description,
            }
        )

    # title length too long
    if len(site.soup.title.string) > site.settings.SEO_SETTINGS["meta_title_length"][1]:
        site.warnings.append(
            {
                "name": long_title_name,
                "settings": long_title_settings,
                "found": len(site.soup.title.string),
                "description": long_title_description,
            }
        )

    title_words = site.soup.title.string.split()

    # title do not contain any keyword
    if set(site.keywords).isdisjoint(set(title_words)):
        site.problems.append(
            {
                "name": keyword_title_name,
                "settings": keyword_title_settings,
                "found": keyword_title_found,
                "description": keyword_title_description,
            }
        )
