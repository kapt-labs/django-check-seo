# Third party
from django.utils.translation import gettext as _

# Local application / specific library imports
from ..checks import custom_list


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Check the length of the url and the maximum depth.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    deep_url = custom_list.CustomList(
        name=_("Too many levels in path"),
        settings=_("less than {}").format(
            site.settings.DJANGO_CHECK_SEO_SETTINGS["max_link_depth"]
        ),
        description=_(
            "Google recommand to organize your content by adding depth in your url, but advises against putting too much depth."
        ),
    )

    long_url = custom_list.CustomList(
        name=_("URL is too long"),
        settings=_("less than {}").format(
            site.settings.DJANGO_CHECK_SEO_SETTINGS["max_url_length"]
        ),
        description=_("Shorter URLs tend to rank better than long URLs."),
    )

    # check url depth
    # do not count first and last slashes (after domain name and at the end of the url), nor // in the "http://"
    url_without_two_points_slash_slash = site.full_url.replace("://", ":..")
    number_of_slashes = url_without_two_points_slash_slash[:-1].count("/")

    deep_url.found = number_of_slashes

    # replace concernet / by underlined /, and put only too mush slashes in red background
    deep_url.searched_in = [
        url_without_two_points_slash_slash.replace(
            "/", '<b><u class="problem">/</u></b>', number_of_slashes
        )
        .replace(":..", "://")
        .replace(
            '<u class="problem">',
            "<u>",
            site.settings.DJANGO_CHECK_SEO_SETTINGS["max_link_depth"],
        )
    ]

    if number_of_slashes > site.settings.DJANGO_CHECK_SEO_SETTINGS["max_link_depth"]:
        site.problems.append(deep_url)
    else:
        deep_url.name = _("Right amount of level in path")
        deep_url.searched_in = [
            url_without_two_points_slash_slash.replace(
                "/", '<b><u class="good">/</u></b>', number_of_slashes
            )
            .replace(":..", "://")
            .replace(
                '<u class="problem">',
                "<u>",
                site.settings.DJANGO_CHECK_SEO_SETTINGS["max_link_depth"],
            )
        ]
        site.success.append(deep_url)

    # check url length
    url_without_protocol = site.full_url.replace("http://", "").replace("https://", "")
    long_url.found = len(url_without_protocol)
    long_url.searched_in = [url_without_protocol]

    if (
        len(url_without_protocol)
        > site.settings.DJANGO_CHECK_SEO_SETTINGS["max_url_length"]
    ):
        site.warnings.append(long_url)
        long_url.searched_in = [
            url_without_protocol[
                : site.settings.DJANGO_CHECK_SEO_SETTINGS["max_url_length"]
            ]
            + '<b class="problem">'
            + url_without_protocol[
                site.settings.DJANGO_CHECK_SEO_SETTINGS["max_url_length"] :
            ]
            + "</b>"
        ]

    else:
        long_url.name = _("URL length is great")
        site.success.append(long_url)
