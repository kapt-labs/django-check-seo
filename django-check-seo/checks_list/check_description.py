# Standard Library
import re

# Third party
from django.utils.translation import gettext as _, ngettext, pgettext

# Local application / specific library imports
from ..checks import custom_list


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):

    settings_length = _("between {rule_low} and {rule_high} chars ").format(
        rule_low=site.settings.SEO_SETTINGS["meta_description_length"][0],
        rule_high=site.settings.SEO_SETTINGS["meta_description_length"][1],
    )
    description = _(
        "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
    )

    name_length_short = custom_list.CustomList(
        name=_("Meta description is too short"),
        settings=settings_length,
        description=description,
    )

    name_length_long = custom_list.CustomList(
        name=_("Meta description is too long"),
        settings=settings_length,
        description=description,
    )

    name_keywords = _("No keyword in meta description")
    description_keywords = _(
        "The meta description tag can be displayed in search results, and the keywords present in the search will be in bold. All this can influence users, and Google ranks sites according to users behaviour."
    )
    settings_keywords = _("at least 1")

    name_present = _("No meta description")
    settings_present = _("needed")
    found_present = pgettext("description", "none")

    name_keywords_good = _("Keywords were found in description")

    too_much_meta = custom_list.CustomList(
        name=_("Too much meta description tags"),
        settings=_("only one"),
        description=_(
            "Although some people write a meta description by targeted keyword, this is still an uncommon practice that is not yet recognized by all search engines."
        ),
    )

    meta = site.soup.find_all("meta")
    found_meta_description = False
    number_meta_description = 0

    for tag in meta:
        if (
            "name" in tag.attrs
            and tag.attrs["name"] == "description"
            and "content" in tag.attrs
            and tag.attrs["content"] != ""
        ):
            number_meta_description += 1
            found_meta_description = True

            length = len(tag.attrs["content"])
            if length < site.settings.SEO_SETTINGS["meta_description_length"][0]:

                name_length_short.found = ngettext(
                    "%(words)d char", "%(words)d chars", length
                ) % {"words": length}
                site.problems.append(name_length_short)

            elif length > site.settings.SEO_SETTINGS["meta_description_length"][1]:

                name_length_long.found = str(length)
                site.problems.append(name_length_long)

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
            print(occurence)
            if not any(i > 0 for i in occurence):
                site.warnings.append(
                    {
                        "name": name_keywords,
                        "settings": settings_keywords,
                        "found": 0,
                        "description": description_keywords,
                    }
                )
            else:
                site.success.append(
                    {
                        "name": name_keywords_good,
                        "settings": settings_present,
                        "found": max(i for i in occurence),
                        "description": description_keywords,
                    }
                )
    if number_meta_description > 1:
        too_much_meta.found = number_meta_description
        site.warnings.append(too_much_meta)

    if not found_meta_description:
        site.problems.append(
            {
                "name": name_present,
                "settings": settings_present,
                "found": found_present,
                "description": description,
            }
        )
