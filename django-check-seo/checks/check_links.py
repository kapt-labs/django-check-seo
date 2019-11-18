# Standard Library
import os

# Third party
import bs4
from django.utils.translation import gettext as _


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Check all link-related conditions
    """
    ne_internal_name = _("Not enough internal links")
    ne_internal_settings = _("more than {}").format(
        site.settings.SEO_SETTINGS["internal_links"]
    )
    ne_internal_description = _(
        "Internal links are useful because they can give the structure of your website to search engines, so they can create a hierarchy of your pages."
    )

    ne_external_name = _("Not enough external links")
    ne_external_settings = _("more than {}").format(
        site.settings.SEO_SETTINGS["external_links"]
    )
    ne_external_description = _(
        "External links help your users to verify your point, and can save them from doing additional research."
    )

    links = bs4.element.ResultSet(None)

    for c in site.content:
        links = c.find_all("a")

    internal_links = 0
    external_links = 0

    for link in links:
        # internal links = absolute links that contains domain name or relative links
        if os.environ["DOMAIN_NAME"] in link["href"] or not link["href"].startswith(
            "http"
        ):
            internal_links += 1
        else:
            external_links += 1

    # not enough internal links
    if internal_links < site.settings.SEO_SETTINGS["internal_links"]:
        site.warnings.append(
            {
                "name": ne_internal_name,
                "settings": ne_internal_settings,
                "found": internal_links,
                "description": ne_internal_description,
            }
        )

    # not enough external links
    if external_links < site.settings.SEO_SETTINGS["external_links"]:
        site.warnings.append(
            {
                "name": ne_external_name,
                "settings": ne_external_settings,
                "found": external_links,
                "description": ne_external_description,
            }
        )
