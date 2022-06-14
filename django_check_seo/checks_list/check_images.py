# Third party
import bs4
from django.utils.translation import gettext as _

# Local application / specific library imports
from ..checks import custom_list


def importance():
    """Scripts with higher importance will be executed first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Checks that each image has a filled alt tag.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    lack_alt = custom_list.CustomList(
        name=_("Images lack alt tag"),
        settings=_("all images"),
        found="",
        description=_(
            'Your images should have an alt tag, because it improves accessibility for visually impaired people.<br />But "<i>sometimes there is non-text content that really is not meant to be seen or understood by the user</i>" (<a href="https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html">WCAG</a>). For this kind of non-text content, you can leave your alt tag empty.<br />The name of the file is important too, because it helps Google understand what your image is about. For example, you could rename a file named "IMG0001.jpg" to "tree_with_a_bird.jpg".'
        ),
    )

    enough_alt = custom_list.CustomList(
        name=_("Images have alt tag"),
        settings=_("all images"),
        found="",
        description=lack_alt.description,
    )

    images = bs4.element.ResultSet(None)

    for c in site.content:
        images += c.find_all("img")

    warning = 0
    imgs = []

    for image in images:
        img_str = image.attrs["src"].split("/")[-1]
        if (
            "alt" not in image.attrs
            or image.attrs["alt"] == "None"
            or image.attrs["alt"] == ""
        ):
            warning += 1

            # bold without alt tag content
            if image.attrs["src"] != "":
                imgs.append(
                    '<b><u class="problem"><a target="_blank" href="'
                    + image.attrs["src"]
                    + '">'
                    + img_str
                    + "</a></u></b>"
                )
            # bold without alt tag content & without src content (dead img ?)
            else:
                imgs.append("<b><u>unknown image</u></b>")

        # normal with alt tag content
        else:
            imgs.append(
                '<a target="_blank" href="'
                + image.attrs["src"]
                + '">'
                + img_str
                + "</a> ("
                + image.attrs["alt"]
                + ")"
            )

    if warning > 0:
        lack_alt.found = warning
        lack_alt.searched_in = imgs
        site.warnings.append(lack_alt)
    else:
        if len(images) > 0:
            enough_alt.found = len(images)
            enough_alt.searched_in = imgs
            site.success.append(enough_alt)
