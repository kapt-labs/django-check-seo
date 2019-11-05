# Third party
from django.utils.translation import gettext as _


def check_keyword_url(site):
    """Check presence of keywords in url
    """
    for keyword in site.keywords:
        if keyword in site.full_url:
            return
    site.problems.append(
        {
            "name": _("No keyword in URL"),
            "settings": _("at least 1"),
            "description": _(
                'Keywords in URL are a small ranking factor for Google (<a href="https://twitter.com/JohnMu/status/1070634500022001666">source</a>), but it will help your users understand the organisation of your website (/?product=50 talk less than /products/camping/). On the other hand Bing says : "<i>URL structure and keyword usage - keep it clean and keyword rich when possible</i>" (<a href="https://www.bing.com/webmaster/help/webmaster-guidelines-30fba23a">source</a>).'
            ),
        }
    )
