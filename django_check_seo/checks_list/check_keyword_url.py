# Standard Library
from urllib.parse import urlparse

import unidecode
from django.conf import settings
from django.conf.global_settings import LANGUAGES
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy

# Local application / specific library imports
from ..checks import custom_list, utils


def importance():
    """Scripts with higher importance will be executed first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Check presence of keywords in url.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    no_keyword = custom_list.CustomList(
        name=_("No keyword in URL"),
        settings=pgettext_lazy("masculin", "at least one"),
        found=pgettext_lazy("masculin", "none"),
        description=_(
            'Keywords in URL will help your users understand the organisation of your website, and are a small ranking factor for Google. On the other hand, Bing guidelines advises to "<i>keep [your URL] clean and keyword rich when possible</i>".<br />Warning, Django Check SEO will try to find keywords in the URL without apostrophes ("pour-lenergie" will be found, but not "pour-l-energie").'
        ),
    )

    enough_keyword = custom_list.CustomList(
        name=_("Keywords found in URL"),
        settings=pgettext_lazy("masculin", "at least one"),
        found="",
        description=no_keyword.description,
    )

    # root url may contain str like "/fr/" or "/en/" if i18n is activated
    url_path = urlparse(site.full_url, "/").path

    # list of languages from django LANGUAGES list: ['fr', 'en', 'br', 'ia', ...]
    languages_list = [i[0] for i in LANGUAGES]

    # do not check keywords in url for root URL
    if (
        (settings.USE_I18N and url_path.replace("/", "") in languages_list)
        or url_path == "/"
        or not url_path
    ):
        return

    full_url = site.full_url.lower()
    occurrence = []
    accented_occurrences = 0

    for keyword in site.keywords:
        keyword = keyword.lower().replace(" ", "-")

        # remove apostrophes as they are removed from URLs
        keyword = keyword.replace("'", "").replace("’", "")

        keyword_unnaccented = unidecode.unidecode(keyword)

        nb_occurrences = utils.count_keyword_occurrences(
            keyword, full_url, for_url=True
        )
        if nb_occurrences == 0:
            # retry with unnaccented kw
            accented_occurrences = utils.count_keyword_occurrences(
                keyword_unnaccented, full_url, for_url=True
            )
        occurrence.append(nb_occurrences + accented_occurrences)

        if nb_occurrences > 0:
            full_url = full_url.replace(keyword, '<b class="good">' + keyword + "</b>")
            if enough_keyword.found != "":
                enough_keyword.found += ", "
            enough_keyword.found += keyword
            nb_occurrences = 0

        if accented_occurrences > 0:
            full_url = full_url.replace(
                keyword_unnaccented, '<b class="good">' + keyword_unnaccented + "</b>"
            )
            if enough_keyword.found != "":
                enough_keyword.found += ", "
            enough_keyword.found += keyword
            accented_occurrences = 0

    if not any(i > 0 for i in occurrence):
        no_keyword.searched_in = [full_url]
        site.problems.append(no_keyword)
    else:
        enough_keyword.searched_in = [full_url]
        site.success.append(enough_keyword)
