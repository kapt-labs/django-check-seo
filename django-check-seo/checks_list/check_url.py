# Third party
from django.utils.translation import gettext as _


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """All the url-related checks.
    """
    deep_url_name_name = _("Too many levels in path")
    deep_url_name_settings = _("less than {}").format(
        site.settings.SEO_SETTINGS["max_link_depth"]
    )
    deep_url_name_description = _(
        "Google recommand to organize your content by adding depth in your url, but advises against putting too much depth."
    )

    long_url_name = _("URL is too long")
    long_url_settings = _("less than {}").format(
        site.settings.SEO_SETTINGS["max_url_length"]
    )
    long_url_description = _("Shorter URLs tend to rank better than long URLs.")

    # check url depth
    # do not count first and last slashes (after domain name and at the end of the url), nor // in the "http://"
    url_without_two_points_slash_slash = site.full_url.replace("://", "")
    number_of_slashes = url_without_two_points_slash_slash.count("/") - 2

    if number_of_slashes > site.settings.SEO_SETTINGS["max_link_depth"]:
        site.problems.append(
            {
                "name": deep_url_name_name,
                "settings": deep_url_name_settings,
                "found": number_of_slashes,
                "description": deep_url_name_description,
            }
        )

    # check url length
    url_without_protocol = site.full_url.replace("http://", "").replace("https://", "")
    if len(url_without_protocol) > site.settings.SEO_SETTINGS["max_url_length"]:
        site.warnings.append(
            {
                "name": long_url_name,
                "settings": long_url_settings,
                "found": len(url_without_protocol),
                "description": long_url_description,
            }
        )
