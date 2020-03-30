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
    return 5


def run(site):
    """Checks that meta tag exists and contain at least one keyword.
    Populate site.keywords list with keywords found.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    no_keywords = custom_list.CustomList(
        name=_("No keywords in meta keywords field"),
        settings=pgettext("masculin", "at least one"),
        found=pgettext("masculin", "none"),
        description=_(
            "Django-check-seo uses the keywords in the meta keywords field to check all other tests related to the keywords. A series of problems and warnings are related to keywords, and will therefore systematically be activated if the keywords are not filled in."
        ),
    )

    keywords_found = custom_list.CustomList(
        name=_("Keywords found in meta keywords field"),
        settings=pgettext("masculin", "at least one"),
        found="",
        description=no_keywords.description,
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

            keywords_found.found = len(site.keywords)
            keywords_found.searched_in = site.keywords
            site.success.append(keywords_found)

            return

    site.problems.append(no_keywords)
