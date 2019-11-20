# Third party
from django.utils.translation import gettext as _


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 5


def run(site):
    """Ensure that meta tag exists and contain at least one keyword.
    Populate site.keywords list with keywords found.
    """
    no_keywords_name = _("No keywords in meta keywords field")
    no_keywords_settings = _("at least 1")
    no_keywords_found = _("none")
    no_keywords_description = _(
        "Django-check-seo uses the keywords in the meta keywords field to check all other tests related to the keywords. A series of problems and warnings are related to keywords, and will therefore systematically be activated if the keywords are not filled in."
    )

    meta = site.soup.find_all("meta")
    for tag in meta:
        if (
            "name" in tag.attrs
            and tag.attrs["name"] == "keywords"
            and "content" in tag.attrs
            and tag.attrs["content"] != ""
        ):
            # get keywords for next checks
            site.keywords = tag.attrs["content"].split(
                ",  "
            )  # may be dangerous to hard code the case where keywords are separated with a comma and two spaces
            return
    site.problems.append(
        {
            "name": no_keywords_name,
            "settings": no_keywords_settings,
            "found": no_keywords_found,
            "description": no_keywords_description,
        }
    )
