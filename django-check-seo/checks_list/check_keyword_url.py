# Third party
# Standard Library
from urllib.parse import urlparse

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Check presence of keywords in url
    """
    no_keyword_name = _("No keyword in URL")
    no_keyword_settings = _("at least 1")
    no_keyword_found = _("none")
    no_keyword_description = _(
        'Keywords in URL will help your users understand the organisation of your website, and are a small ranking factor for Google. On the other hand, Bing guidelines advises to "<i>keep [your URL] clean and keyword rich when possible</i>".'
    )

    # root url may contain str like "/fr/" or "/en/" if i18n is activated
    url_path = urlparse(site.full_url, "/").path

    if (
        settings.USE_I18N
        and url_path == "/{lang}/".format(lang=translation.get_language())
    ) or url_path == "/":
        return

    for keyword in site.keywords:
        if keyword in site.full_url:
            return
    site.problems.append(
        {
            "name": no_keyword_name,
            "settings": no_keyword_settings,
            "found": no_keyword_found,
            "description": no_keyword_description,
        }
    )
