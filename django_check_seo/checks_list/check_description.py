# Standard Library
import re

# Third party
from django.utils.translation import gettext as _
from django.utils.translation import ngettext, pgettext

# Local application / specific library imports
from ..checks import custom_list


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Checks that only one meta description tag is present in the page, that it is the right length and that it contains at least one keyword.

    Arguments:
        site {Site} -- Structure containing a good amount of resources from the targeted webpage.
    """
    length_short = custom_list.CustomList(
        name=_("Meta description is too short"),
        settings=_("between {rule_low} and {rule_high} chars ").format(
            rule_low=site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_description_length"][
                0
            ],
            rule_high=site.settings.DJANGO_CHECK_SEO_SETTINGS[
                "meta_description_length"
            ][1],
        ),
        description=_(
            "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
        ),
    )

    length_long = custom_list.CustomList(
        name=_("Meta description is too long"),
        settings=length_short.settings,
        description=length_short.description,
    )

    length_success = custom_list.CustomList(
        name=_("Meta description length is correct"),
        settings=length_short.settings,
        description=length_short.description,
    )

    keywords_bad = custom_list.CustomList(
        name=_("No keyword in meta description"),
        settings=pgettext("masculin", "at least one"),
        description=length_short.description,
    )

    keywords_good = custom_list.CustomList(
        name=_("Keywords were found in meta description"),
        settings=pgettext("masculin", "at least one"),
        description=length_short.description,
    )

    too_much_meta = custom_list.CustomList(
        name=_("Too much meta description tags"),
        settings=pgettext("feminin", "only one"),
        description=_(
            "Although some people write one meta description by targeted keyword, this is still an uncommon practice that is not yet recognized by all search engines."
        ),
    )

    meta_description_only_one = custom_list.CustomList(
        name=_("Only one meta description tag"),
        settings=pgettext("feminin", "only one"),
        found=pgettext("feminin", "one"),
        description=too_much_meta.description,
    )

    no_meta_description = custom_list.CustomList(
        name=_("No meta description"),
        settings=pgettext("feminin", "needed"),
        found=pgettext("description", "none"),
        description=length_short.description,
    )

    meta_description_present = custom_list.CustomList(
        name=_("Meta description is present"),
        settings=pgettext("feminin", "needed"),
        found=pgettext("feminin", "one"),
        description=_(
            "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
        ),
    )

    meta = site.soup.find_all("meta")
    found_meta_description = False
    number_meta_description = 0
    meta_description = []
    meta_description_kw = []

    for tag in meta:
        if (
            "name" in tag.attrs
            and tag.attrs["name"] == "description"
            and "content" in tag.attrs
            and tag.attrs["content"] != ""
        ):
            number_meta_description += 1
            found_meta_description = True

            meta_description.append(tag.attrs["content"])
            meta_description_kw.append(
                meta_description[number_meta_description - 1].lower()
            )
            length = len(tag.attrs["content"])

            # too short
            if (
                length
                < site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_description_length"][0]
            ):

                length_short.found = ngettext(
                    "%(words)d char", "%(words)d chars", length
                ) % {"words": length}
                length_short.searched_in = meta_description
                site.problems.append(length_short)

            # too long
            elif (
                length
                > site.settings.DJANGO_CHECK_SEO_SETTINGS["meta_description_length"][1]
            ):

                length_long.found = str(length)
                length_long.searched_in = [
                    tag.attrs["content"][
                        : site.settings.DJANGO_CHECK_SEO_SETTINGS[
                            "meta_description_length"
                        ][1]
                    ]
                    + '<b class="problem">'
                    + tag.attrs["content"][
                        site.settings.DJANGO_CHECK_SEO_SETTINGS[
                            "meta_description_length"
                        ][1] :
                    ]
                    + "</b>"
                ]
                site.problems.append(length_long)

            # perfect
            else:

                length_success.found = str(length)
                length_success.searched_in = meta_description
                site.success.append(length_success)

            occurrence = []
            keywords_good.found = ""
            for keyword in site.keywords:
                keyword_lower = keyword.lower()
                nb_occurrences = len(
                    re.findall(
                        r"(^| |\n|,|\.|!|\?)" + keyword_lower + r"($| |\n|,|\.|!|\?)",
                        tag.attrs["content"].lower(),
                    )
                )
                occurrence.append(nb_occurrences)
                # edit current meta description
                meta_description_kw[number_meta_description - 1] = meta_description_kw[
                    number_meta_description - 1
                ].replace(keyword_lower, '<b class="good">' + keyword_lower + "</b>")

                # add kw in found keywords
                if nb_occurrences > 0:
                    if keywords_good.found != "":
                        keywords_good.found += ", "
                    keywords_good.found += keyword

            # if no keyword is found in description
            if not any(i > 0 for i in occurrence):

                keywords_bad.found = 0
                keywords_bad.searched_in = meta_description
                site.warnings.append(keywords_bad)

            # perfect
            else:
                keywords_good.searched_in = meta_description_kw
                site.success.append(keywords_good)

    # too many meta description
    if number_meta_description > 1:

        too_much_meta.found = number_meta_description
        too_much_meta.searched_in = meta_description
        site.warnings.append(too_much_meta)

    # perfect
    else:
        meta_description_only_one.searched_in = meta_description
        site.success.append(meta_description_only_one)

    # no meta description
    if not found_meta_description:
        site.problems.append(no_meta_description)

    # perfect
    else:
        meta_description_present.searched_in = meta_description
        site.success.append(meta_description_present)
