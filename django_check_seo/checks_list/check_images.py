# Third party
import bs4
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
    """Checks that each image has a filled alt tag.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """

    lack_alt = custom_list.CustomList(
        name=_("Img lack alt tag"),
        settings=_("all images"),
        found="",
        description=_(
            'Your images should always have an alt tag, because it improves accessibility for visually impaired people. The name of the file is important too, because it helps Google understand what your image is about. For example, you could rename a file named "IMG0001.jpg" to "tree_with_a_bird.jpg".'
        ),
    )

    enough_alt = custom_list.CustomList(
        name=_("Img have alt tag"),
        settings=_("all images"),
        found="",
        description=lack_alt.description,
    )

    images = bs4.element.ResultSet(None)

    for c in site.content:
        images += c.find_all("img")

    problem = 0
    imgs = []
    img_str = _("image")

    for image in images:
        if (
            "alt" not in image.attrs
            or image.attrs["alt"] == "None"
            or image.attrs["alt"] == ""
        ):
            problem += 1

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

    if problem > 0:
        lack_alt.found = problem
        lack_alt.searched_in = imgs
        site.problems.append(lack_alt)
    else:
        if len(images) > 0:
            enough_alt.found = len(images)
            enough_alt.searched_in = imgs
            site.success.append(enough_alt)
