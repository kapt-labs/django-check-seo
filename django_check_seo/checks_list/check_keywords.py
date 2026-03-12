# Third party
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy

# Local application / specific library imports
from ..checks import custom_list


def importance():
    """Scripts with higher importance will be executed first.

    Returns:
        int -- Importance of the script.
    """
    return 5


def run(site):
    """Validate that at least one keyword is defined for this page.

    site.keywords is expected to be already populated by the configured
    keywords discovery method (meta or model). This check only validates
    presence and reports success or problem with generic labels.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    no_keywords = custom_list.CustomList(
        name=_("No keywords defined for this page"),
        settings=pgettext_lazy("masculin", "at least one"),
        found=pgettext_lazy("masculin", "none"),
        description=_(
            "Django-check-seo uses the keywords to check all other tests related to them. "
            "A series of problems and warnings are related to keywords, and will therefore "
            "systematically be activated if the keywords are not filled in."
        ),
    )

    keywords_found = custom_list.CustomList(
        name=_("Keywords found"),
        settings=pgettext_lazy("masculin", "at least one"),
        found="",
        description=no_keywords.description,
    )

    if not site.keywords or len(site.keywords) == 0:
        site.problems.append(no_keywords)
        return

    keywords_found.found = len(site.keywords)
    keywords_found.searched_in = site.keywords
    site.success.append(keywords_found)
