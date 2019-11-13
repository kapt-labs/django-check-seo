# Standard Library
import re

# Third party
from django.utils.translation import gettext as _, ngettext, pgettext


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    name_length_short = _("Meta description is too short")
    name_length_long = _("Meta description is too long")
    description = _(
        "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
    )
    settings_length = _("between {rule_low} and {rule_high} chars ").format(
        rule_low=site.settings.SEO_SETTINGS["meta_description_length"][0],
        rule_high=site.settings.SEO_SETTINGS["meta_description_length"][1],
    )

    name_keywords = _("No keyword in meta description")
    description_keywords = _(
        "The meta description tag can be displayed in search results, and the keywords present in the search will be in bold. All this can influence users, and Google ranks sites according to users behaviour."
    )
    settings_keywords = "at least 1"

    name_present = _("No meta description")
    settings_present = "needed"
    found_present = pgettext("description", "none")

    meta = site.soup.find_all("meta")
    for tag in meta:
        if (
            "name" in tag.attrs
            and tag.attrs["name"] == "description"
            and "content" in tag.attrs
            and tag.attrs["content"] != ""
        ):
            length = len(tag.attrs["content"])
            if length < site.settings.SEO_SETTINGS["meta_description_length"][0]:
                site.problems.append(
                    {
                        "name": name_length_short,
                        "settings": settings_length,
                        "found": ngettext("%(words)d char", "%(words)d chars", length)
                        % {"words": length},
                        "description": description,
                    }
                )
            elif length > site.settings.SEO_SETTINGS["meta_description_length"][1]:
                site.problems.append(
                    {
                        "name": name_length_long,
                        "settings": settings_length,
                        "found": str(length),
                        "description": description,
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
                        "name": name_keywords,
                        "settings": settings_keywords,
                        "found": 0,
                        "description": description_keywords,
                    }
                )

            return
    site.problems.append(
        {
            "name": name_present,
            "settings": settings_present,
            "found": found_present,
            "description": description,
        }
    )
