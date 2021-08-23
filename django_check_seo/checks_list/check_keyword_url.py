# Standard Library
import re
import sys

import unidecode
from django.conf import settings
from django.conf.global_settings import LANGUAGES
from django.utils.translation import gettext as _
from django.utils.translation import pgettext

# Local application / specific library imports
from ..checks import custom_list

# hacky trick to add python2 compatibility to a python3 project after python2 eol
if sys.version_info.major == 2:
    from urlparse import urlparse  # pragma: no cover
else:
    from urllib.parse import urlparse  # pragma: no cover


def importance():
    """Scripts with higher importance will be executed in first.

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
        settings=pgettext("masculin", "at least one"),
        found=pgettext("masculin", "none"),
        description=_(
            'Keywords in URL will help your users understand the organisation of your website, and are a small ranking factor for Google. On the other hand, Bing guidelines advises to "<i>keep [your URL] clean and keyword rich when possible</i>".'
        ),
    )

    enough_keyword = custom_list.CustomList(
        name=_("Keywords found in URL"),
        settings=pgettext("masculin", "at least one"),
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
        keyword = keyword.lower()
        # needed for python2, see https://stackoverflow.com/a/21129492/6813732
        if sys.version_info.major == 2:
            keyword_unnaccented = unidecode.unidecode(
                unicode(keyword, "utf-8").replace(" ", "-")  # noqa F821
            )  # pragma: no cover
        else:
            keyword_unnaccented = unidecode.unidecode(keyword).replace(
                " ", "-"
            )  # pragma: no cover
        nb_occurrences = len(
            re.findall(
                r"(^| |\n|,|\.|!|\?|/|-)" + keyword + r"($| |\n|,|\.|!|\?|/|-)",
                full_url,
            )
        )
        if nb_occurrences == 0:
            # retry with unnaccented kw
            accented_occurrences = len(
                re.findall(
                    r"(^| |\n|,|\.|!|\?|/|-)"
                    + keyword_unnaccented
                    + r"($| |\n|,|\.|!|\?|/|-)",
                    full_url,
                )
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
