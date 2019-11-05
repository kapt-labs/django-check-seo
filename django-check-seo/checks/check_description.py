# Standard Library
import re

# Third party
from django.utils.translation import gettext as _


def check_description(site):
    meta = site.soup.find_all("meta")
    for tag in meta:
        if (
            "name" in tag.attrs
            and tag.attrs["name"] == "description"
            and "content" in tag.attrs
            and tag.attrs["content"] != ""
        ):
            if (
                len(tag.attrs["content"])
                < site.settings.SEO_SETTINGS["meta_description_length"][0]
            ):
                site.problems.append(
                    {
                        "name": _("Meta description is too short"),
                        "settings": _(
                            "&gt;{rule} chars, found {words}".format(
                                rule=site.settings.SEO_SETTINGS[
                                    "meta_description_length"
                                ][0],
                                words=len(tag.attrs["content"]),
                            )
                        ),
                        "description": _(
                            "Meta description can be displayed below your page title in search results. If Google find your description too short or not relevant, it will generate it's own description, based on your page content. This generated description will be less accurate than a good writen description."
                        ),
                    }
                )
            elif (
                len(tag.attrs["content"])
                > site.settings.SEO_SETTINGS["meta_description_length"][1]
            ):
                site.problems.append(
                    {
                        "name": _("Meta description is too long"),
                        "settings": _(
                            "&lt;{rule} chars, found {words}".format(
                                rule=site.settings.SEO_SETTINGS[
                                    "meta_description_length"
                                ][1],
                                words=len(tag.attrs["content"]),
                            )
                        ),
                        "description": _(
                            "Meta description can be displayed below your page title in search results. If Google find your description too long, it may crop it and your potential visitors will not be able to read all its content. Sometimes, long pertinent meta descriptions will be displayed, but in the vast majority of the results, the description's lengths are 150-170 chars."
                        ),
                    }
                )

            occurence = []
            for keyword in site.keywords:
                occurence.append(
                    sum(
                        1
                        for _ in re.finditer(
                            r"\b%s\b" % re.escape(keyword.lower()),
                            tag.attrs["content"].lower(),
                        )
                    )
                )
            # if no keyword is found in h1
            if not any(i > 0 for i in occurence):
                site.warnings.append(
                    {
                        "name": _("No keyword in meta description"),
                        "settings": _("at least 1"),
                        "description": _(
                            "Meta description is not used by search engines to calculate the rank of the page, but users will read it (if the meta description is selected by Google). The bonus point is that Google will put the keywords searched by the users in bold, so the users can eaily verify that the content of your page fit their needs."
                        ),
                    }
                )

            return
    site.problems.append(
        {
            "name": _("No meta description"),
            "settings": _("needed"),
            "description": _(
                'Even if search engines states that they don\'t use meta description for ranking (<a href="https://webmasters.googleblog.com/2009/09/google-does-not-use-keywords-meta-tag.html">source</a>), they can be displayed below the title of your page in search results. Since search engines uses users clics to rank your website, an appealing description can make the difference.<br />Google has affirmed that they display a shorter text (~155 chars) below the title of the page (<a href="https://twitter.com/dannysullivan/status/996065145443893249">source</a>).'
            ),
        }
    )
