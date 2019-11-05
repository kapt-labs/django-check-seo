# Third party
from django.utils.translation import gettext as _


def check_url(site):
    """All the url-related checks.
    """

    # check url depth
    # do not count first slash after domain name, nor // in the "http://"
    url_without_two_points_slash_slash = site.full_url.replace("://", "")
    number_of_slashes = url_without_two_points_slash_slash.count("/") - 1

    if number_of_slashes > site.settings.SEO_SETTINGS["max_link_depth"]:
        site.problems.append(
            {
                "name": _("Too many levels in path"),
                "settings": "&le;{settings}, found {path_depth}".format(
                    settings=site.settings.SEO_SETTINGS["max_link_depth"],
                    path_depth=number_of_slashes,
                ),
                "description": _(
                    'Google recommand to organize your content by adding depth in your url, but advises against putting too much repertories (<a href="https://support.google.com/webmasters/answer/7451184">source</a>).<br />Yoast says that "In a perfect world, we would place everything in one sublevel at most. Today, many sites use secondary menus to accommodate for additional content" (<a href="https://yoast.com/how-to-clean-site-structure/">source</a>).'
                ),
            }
        )

    # check url length
    url_without_protocol = site.full_url.replace("http://", "").replace("https://", "")
    if len(url_without_protocol) > site.settings.SEO_SETTINGS["max_url_length"]:
        site.warnings.append(
            {
                "name": _("URL is too long"),
                "settings": "&le;{settings}, found {len_url} chars".format(
                    settings=site.settings.SEO_SETTINGS["max_url_length"],
                    len_url=len(url_without_protocol),
                ),
                "description": _(
                    'A study from 2016 found a correlation between URL length & ranking (<a href="https://backlinko.com/search-engine-ranking">source</a>).'
                ),
            }
        )
