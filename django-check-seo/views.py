# Standard Library
import json
import os

# Third party
from bs4 import BeautifulSoup
from django.utils.translation import gettext as _, ngettext
from django.views import generic
import requests

# Local application / specific library imports
from .conf import settings


class IndexView(generic.base.TemplateView):
    template_name = "default.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        full_url = os.environ["DOMAIN_NAME"] + self.request.GET.get("page", None)
        # do not get cached page (useful ?)
        r = requests.get("http://" + full_url, headers={"Cache-Control": "no-cache"})
        context["parsehtml"] = r.text
        soup = BeautifulSoup(r.text, features="lxml")

        context["settings"] = json.dumps(settings.SEO_SETTINGS, indent=4)

        django_check_seo = DjangoCheckSeo(soup)
        (context["problems"], context["warnings"]) = django_check_seo.check()

        return context


class DjangoCheckSeo:
    def __init__(self, soup):
        self.soup = soup
        self.keywords = []
        self.problems = []
        self.warnings = []

    def check(self):
        self.check_keywords()
        self.check_title()

        return (self.problems, self.warnings)

    # first check to ensure that keywords are present
    def check_keywords(self):
        meta = self.soup.find_all("meta")
        for tag in meta:
            if tag.attrs["name"] == "keywords" and tag.attrs["content"] != "":
                # get keywords for next checks
                self.keywords = tag.attrs["content"].split(
                    ",  "
                )  # may be dangerous to hard code the case where keywords are separated with a comma and two spaces
                print(self.keywords)
                return
        self.problems.append(
            {
                "name": _("No meta keywords"),
                "description": _(
                    "Meta keywords were important in this meta tag, however django-check-seo uses these keywords to check all other tests related to keywords. You will be flooded with problems and warnings and this SEO tool will not work as well as it should if you don't add some keywords."
                ),
            }
        )

    def check_title(self):
        # title presence
        if self.soup.title == "None":
            self.problems.append(
                {
                    "name": _("No title tag"),
                    "description": _(
                        "Titles tags are ones of the most important things to add to your pages, sinces they are the main text displayed on result search pages."
                    ),
                }
            )
            return

        # title length too short
        if len(self.soup.title.string) <= settings.SEO_SETTINGS["meta_title_length"][0]:
            self.problems.append(
                {
                    "name": _("Title tag is too short"),
                    "description": _(
                        "Titles tags need to describe the content of the page, and need to contain at least a few words (settings: >="
                    )
                    + ngettext(
                        "{title_length} word",
                        "{title_length} words",
                        settings.SEO_SETTINGS["meta_title_length"][0],
                    ).format(settings.SEO_SETTINGS["meta_title_length"][0])
                    + ").",
                }
            )

        # title length too long
        if len(self.soup.title.string) >= settings.SEO_SETTINGS["meta_title_length"][1]:
            self.warnings.append(
                {
                    "name": _("Title tag is too long"),
                    "description": _(
                        "Only the first ~55-60 chars are displayed on modern search engines results. Writing a longer title is not really required and can lead to make the user miss informations."
                    ),
                }
            )

        title_words = self.soup.title.string.split()

        # title do not contain any keyword
        if set(self.keywords).isdisjoint(set(title_words)):
            self.problems.append(
                {
                    "name": _("Title do not contain any keyword"),
                    "description": _("Titles tags need to contain some keywords."),
                }
            )
