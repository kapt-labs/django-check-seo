# Third party
# Standard Library
import sys

from django.conf import settings
from django.conf.global_settings import LANGUAGES
from django.utils.text import slugify
from django.utils.translation import gettext as _, pgettext

# Local application / specific library imports
from ..checks import custom_list


# hacky trick to add python2 compatibility to a python3 project after python2 eol
if sys.version_info.major == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse


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

    keyword_found = False

    for keyword in site.keywords:
        if slugify(keyword) in site.full_url:
            if keyword_found:
                enough_keyword.found += ", "
            keyword_found = True
            enough_keyword.found += keyword

    if keyword_found:
        enough_keyword.searched_in = [site.full_url]
        site.success.append(enough_keyword)
    else:
        no_keyword.searched_in = [site.full_url]
        site.problems.append(no_keyword)
