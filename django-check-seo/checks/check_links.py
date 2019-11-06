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
    if internal_links < site.settings.SEO_SETTINGS["internal_links"][0]:
        site.warnings.append(
            {
                "name": _("Not enough internal links"),
                "settings": "&ge;{}".format(
                    site.settings.SEO_SETTINGS["internal_links"][0]
                ),
                "description": _(
                    "Internal links are useful because they link your content and can give any search engine the structure of your website, so they can create a hierarchy of your pages."
                ),
            }
        )

    # too much internal links
    if internal_links > site.settings.SEO_SETTINGS["internal_links"][1]:
        site.warnings.append(
            {
                "name": _("Too many internal links"),
                "settings": "&le;{}".format(
                    site.settings.SEO_SETTINGS["internal_links"][1]
                ),
                "description": _(
                    'Google is vague about the max number of internal links on your site. <a href="https://neilpatel.com/blog/commandments-of-internal-linking/">Neil Patel</a> advises 3 to 4 internal links in the content of your page (excluding header/footer), but he says that you can go up to 10-20 links if your content is long enough.'
                ),
            }
        )

    # not enough external links
    if external_links < site.settings.SEO_SETTINGS["external_links"][0]:
        site.warnings.append(
            {
                "name": _("Not enough external links"),
                "settings": "&ge;{}".format(
                    site.settings.SEO_SETTINGS["external_links"][0]
                ),
                "description": _(
                    'Some recent SEO-related articles advise you to add some external links to help SEO on other websites (<a href="https://yoast.com/outbound-links/">source</a>) while at the other end an old (2015) study found that links to websites with an high authority help incresing websites ranking (<a href="https://www.rebootonline.com/blog/long-term-outgoing-link-experiment/">source</a>).'
                ),
            }
        )

    # too much external links
    if external_links > site.settings.SEO_SETTINGS["external_links"][1]:
        site.warnings.append(
            {
                "name": _("Too many external links"),
                "settings": "&le;{}".format(
                    site.settings.SEO_SETTINGS["external_links"][1]
                ),
                "description": _(
                    '"Thanks to updates like Google Penguin, Google now focuses on link quality (not just link quantity)". There\'s no need to have too many external links on your main content, but the reputation of the websites you are linking to is important.'
                ),
            }
        )
