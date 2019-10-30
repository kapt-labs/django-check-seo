# Standard Library
import json
import os
import re

# Third party
from bs4 import BeautifulSoup
from django.utils.translation import gettext as _
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

        django_check_seo = DjangoCheckSeo(soup, full_url)
        (context["problems"], context["warnings"]) = django_check_seo.check()

        return context


class DjangoCheckSeo:
    def __init__(self, soup, full_url):
        """Populate some vars.

        Arguments:
            soup {bs4.element} -- beautiful soup content (html)
        """
        self.soup = soup
        # Get content of the page (exclude header/footer)
        self.content = self.soup.find("div", {"class": "container"})
        # remove ul with nav class from content (<ul class="nav"> is the menu)
        self.content.find("ul", {"class": "nav"}).extract()
        self.full_url = full_url
        self.keywords = []
        self.problems = []
        self.warnings = []

    def check(self):
        self.check_keywords()
        self.check_title()
        self.check_links()
        self.check_keyword_occurence()
        self.check_keyword_url()
        self.check_h1()

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
                return
        self.problems.append(
            {
                "name": _("No meta keywords"),
                "settings": _("at least 1"),
                "description": _(
                    "Meta keywords were important in this meta tag, however django-check-seo uses these keywords to check all other tests related to keywords. You will be flooded with problems and warnings and this SEO tool will not work as well as it should if you don't add some keywords."
                ),
            }
        )

    def check_title(self):
        """Check all title-related conditions
        """
        # title presence
        if self.soup.title == "None":
            self.problems.append(
                {
                    "name": _("No title tag"),
                    "settings": _("at least 1"),
                    "description": _(
                        "Titles tags are ones of the most important things to add to your pages, sinces they are the main text displayed on result search pages."
                    ),
                }
            )
            return

        # title length too short
        if len(self.soup.title.string) < settings.SEO_SETTINGS["meta_title_length"][0]:
            self.problems.append(
                {
                    "name": _("Title tag is too short"),
                    "settings": "&ge;{}".format(
                        settings.SEO_SETTINGS["meta_title_length"][0]
                    ),
                    "description": _(
                        "Titles tags need to describe the content of the page, and need to contain at least a few words."
                    ),
                }
            )

        # title length too long
        if len(self.soup.title.string) > settings.SEO_SETTINGS["meta_title_length"][1]:
            self.warnings.append(
                {
                    "name": _("Title tag is too long"),
                    "settings": "&le;{}".format(
                        settings.SEO_SETTINGS["meta_title_length"][1]
                    ),
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
                    "settings": _("at least 1"),
                    "description": _("Titles tags need to contain some keywords."),
                }
            )

    def check_links(self):
        """Check all link-related conditions
        """
        links = self.content.find_all("a")
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
        if internal_links < settings.SEO_SETTINGS["internal_links"][0]:
            self.problems.append(
                {
                    "name": _("Not enough internal links"),
                    "settings": "&ge;{}".format(
                        settings.SEO_SETTINGS["internal_links"][0]
                    ),
                    "description": _(
                        "Internal links are useful because they link your content and can give any search engine the structure of your website, so they can create a hierarchy of your pages."
                    ),
                }
            )

        # too much internal links
        if internal_links > settings.SEO_SETTINGS["internal_links"][1]:
            self.problems.append(
                {
                    "name": _("Too many internal links"),
                    "settings": "&le;{}".format(
                        settings.SEO_SETTINGS["internal_links"][1]
                    ),
                    "description": _(
                        'Google is vague about the max number of internal links on your site. <a href="https://neilpatel.com/blog/commandments-of-internal-linking/">Neil Patel</a> advises 3 to 4 internal links in the content of your page (excluding header/footer), but he says that you can go up to 10-20 links if your content is long enough.'
                    ),
                }
            )

        # not enough external links
        if external_links < settings.SEO_SETTINGS["external_links"][0]:
            self.problems.append(
                {
                    "name": _("Not enough external links"),
                    "settings": "&ge;{}".format(
                        settings.SEO_SETTINGS["external_links"][0]
                    ),
                    "description": _(
                        'Some recent SEO-related articles advise you to add some external links to help SEO on other websites (<a href="https://yoast.com/outbound-links/">source</a>) while at the other end an old (2015) study found that links to websites with an high authority help incresing websites ranking (<a href="https://www.rebootonline.com/blog/long-term-outgoing-link-experiment/">source</a>).'
                    ),
                }
            )

        # too much external links
        if external_links > settings.SEO_SETTINGS["external_links"][1]:
            self.problems.append(
                {
                    "name": _("Too many external links"),
                    "settings": "&le;{}".format(
                        settings.SEO_SETTINGS["external_links"][1]
                    ),
                    "description": _(
                        '"Thanks to updates like Google Penguin, Google now focuses on link quality (not just link quantity)". There\'s no need to have too many external links on your main content, but the reputation of the websites you are linking to is important.'
                    ),
                }
            )

    def check_keyword_occurence(self):
        """Check if one of the keywords is present between keywords_repeat[0] & keywords_repeat[1] in the page. If no keywords is in this range, then will fire a problem.
        no case sensitive (keyword & text are lowered before comparison).
        Thx https://stackoverflow.com/a/17268979/6813732 for finditer.
        """
        occurence = []
        for keyword in self.keywords:
            occurence.append(
                sum(
                    1
                    for _ in re.finditer(
                        r"\b%s\b" % re.escape(keyword.lower()),
                        self.content.text.lower(),
                    )
                )
            )

        # if no keyword is repeated more than ["keywords_repeat"][0]
        if not any(i >= settings.SEO_SETTINGS["keywords_repeat"][0] for i in occurence):
            self.problems.append(
                {
                    "name": _("Not enough keyword repeat"),
                    "settings": "&ge;{}".format(
                        settings.SEO_SETTINGS["keywords_repeat"][0]
                    ),
                    "description": _(
                        'Presence of keywords are important for search engines like Google, who will "understand" what your content is about, and will better serve your page in answer to structured queries that uses your keywords.'
                    ),
                }
            )
        # there is at least 1 keyword that is repeated > ["keywords_repeat"][0]
        else:
            # there is at least 1 keyword that is repeated > ["keywords_repeat"][1]
            if not all(
                i < settings.SEO_SETTINGS["keywords_repeat"][1] for i in occurence
            ):
                self.problems.append(
                    {
                        "name": _("Too many keyword repeat"),
                        "settings": "&le;{}".format(
                            settings.SEO_SETTINGS["keywords_repeat"][1]
                        ),
                        "description": _(
                            "Some SEO websites advise you to get 1% of your words to be keywords. For other websites (like Yoast) it's 0.25-0.5%. We use a constant for keywords repetition. Too many keywords on a page will lead search engines to think that you're doing some keyword stuffing (put too many keywords in order to manipulate the page rank)."
                        ),
                    }
                )

    def check_keyword_url(self):
        """Check presence of keywords in url
        """
        for keyword in self.keywords:
            if keyword in self.full_url:
                return
        self.problems.append(
            {
                "name": _("No keyword in URL"),
                "settings": _("at least 1"),
                "description": _(
                    'Keywords in URL are a small ranking factor for Google (<a href="https://twitter.com/JohnMu/status/1070634500022001666">source</a>), but it will help your users understand the organisation of your website (/?product=50 talk less than /products/camping/). On the other hand Bing says : "<i>URL structure and keyword usage - keep it clean and keyword rich when possible</i>" (<a href="https://www.bing.com/webmaster/help/webmaster-guidelines-30fba23a">source</a>).'
                ),
            }
        )

    def check_h1(self):
        """Check all h1-related conditions
        """

        h1 = self.soup.find_all("h1")
        if len(h1) > 1:
            self.problems.append(
                {
                    "name": _("Too much h1 tags"),
                    "settings": _("exactly 1"),
                    "description": _(
                        'Google has told that they do not consider using multiple h1 a bad thing (<a href="https://www.youtube.com/watch?v=WsgrSxCmMbM">source</a>), but Google is not the unique search engine out there. Bing webmaster guidelines says "Use only one <H1> tag per page".'
                    ),
                }
            )

        elif not h1:
            self.problems.append(
                {
                    "name": _("No h1 tag"),
                    "settings": _("exactly 1"),
                    "description": _(
                        "H1 is the most visually notable content of your page for your users, and is one of the most important ranking factor for search engines. A good h1 tag content is required in order to progress in SERP."
                    ),
                }
            )

        else:
            occurence = []
            for keyword in self.keywords:
                occurence.append(
                    sum(
                        1
                        for _ in re.finditer(
                            r"\b%s\b" % re.escape(keyword.lower()),
                            self.content.text.lower(),
                        )
                    )
                )
            # if no keyword is found in h1
            if not any(i > 0 for i in occurence):
                self.problems.append(
                    {
                        "name": _("No keyword in h1"),
                        "settings": _("at least 1"),
                        "description": _(
                            "H1 are crawled by search engines as the title of your page. You may populate them with appropriate content in order to be sure that search engines correctly understand what your pages are all about."
                        ),
                    }
                )
