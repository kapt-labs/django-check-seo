# Standard Library
import json
import os
import re

# Third party
from bs4 import BeautifulSoup
from django.views import generic
import requests

# Local application / specific library imports
from .checks import launch_checks
from .conf import settings


class IndexView(generic.base.TemplateView):
    template_name = "default.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # get http content of the page

        if "http" not in self.request.GET.get("page", None):
            full_url = (
                "http://"
                + os.environ["DOMAIN_NAME"]
                + self.request.GET.get("page", None)
            )
        else:
            full_url = self.request.GET.get("page", None)

        # do not get cached page (useful ?)
        r = requests.get(full_url, headers={"Cache-Control": "no-cache"})

        soup = BeautifulSoup(r.text, features="lxml")

        # populate class with data
        site = Site(soup, full_url)

        # magic happens here!
        launch_checks.launch_checks(site)

        (context["problems"], context["warnings"]) = (site.problems, site.warnings)

        context["parsehtml"] = r.text
        context["settings"] = json.dumps(settings.SEO_SETTINGS, indent=4)
        context["contenthtml"] = site.content
        context["content"] = site.content_text

        return context


class Site:
    """Structure containing a good amount of resources from the targeted webpage:
    - the settings
    - the soup (from beautifulsoup)
    - the content (all html except header & menu)
    - the full url
    - the keywords
    - the problems & warnings
    """

    def __init__(self, soup, full_url):
        """Populate some vars.

        Arguments:
            soup {bs4.element} -- beautiful soup content (html)
            full_url {str} -- full url
        """
        self.settings = settings

        self.soup = soup

        # Get content of the page (exclude header/footer)
        self.content = self.soup.find("div", {"class": "container"})
        if self.content is None:
            self.content = ""

        # remove ul with nav class from content (<ul class="nav">, <ul class="navbar">, or <nav>)
        if self.content.find("ul", {"class": "nav"}):
            self.content.find("ul", {"class": "nav"}).extract()
        elif self.content.find("ul", {"class": "navbar"}):
            self.content.find("ul", {"class": "navbar"}).extract()
        elif self.content.find("nav"):
            self.content.find("nav").extract()

        # get content without doublewords thx to separator ("<h1>Title</h1><br /><p>Content</p>" -> TitleContent)
        self.content_text = self.content.get_text(separator=" ")
        # strip multiple carriage return (with optional space) to only one
        self.content_text = re.sub(r"(\n( ?))+", "\n", self.content_text)
        # strip multiples spaces (>3) to only 2 (for title readability)
        self.content_text = re.sub(r"   +", "  ", self.content_text)

        self.full_url = full_url
        self.keywords = []
        self.problems = []
        self.warnings = []
