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

    images = bs4.element.ResultSet(None)

    for c in site.content:
        images += c.find_all("img")

    for image in images:
        if "alt" not in image.attrs or image.attrs["alt"] == "None":
            site.problems.append(
                {
                    "name": _("Img lack alt tag"),
                    "settings": _("all images"),
                    "description": _(
                        'Your images should always have an alt tag, because it improves accessibility for visually impaired people.<br />The name of your image is important too, because Google will look at it to know what the picture is about (<a href="https://support.google.com/webmasters/answer/114016">source</a>).<br /><a href="{img_url}">This is the image</a> without alt tag.'.format(
                            img_url=image.attrs["src"]
                        )
                    ),
                }
            )
