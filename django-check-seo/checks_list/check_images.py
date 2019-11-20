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

    lack_alt_name = _("Img lack alt tag")
    lack_alt_settings = _("all images")
    lack_alt_description = _(
        'Your images should always have an alt tag, because it improves accessibility for visually impaired people. The name of the file is important too, because it helps Google understand what your image is about. For example, you could rename a file named "IMG0001.jpg" to "tree_with_a_bird.jpg".'
    )
    lack_alt_found = "this image"

    images = bs4.element.ResultSet(None)

    for c in site.content:
        images += c.find_all("img")

    for image in images:
        if "alt" not in image.attrs or image.attrs["alt"] == "None":
            site.problems.append(
                {
                    "name": lack_alt_name,
                    "settings": lack_alt_settings,
                    "found": '<a target="_blank" href="{img_url}">{lack_alt_found}</a>'.format(
                        img_url=image.attrs["src"], lack_alt_found=lack_alt_found
                    ),
                    "description": lack_alt_description,
                }
            )
