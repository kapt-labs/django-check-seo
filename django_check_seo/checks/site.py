# Standard Library
import re

# Local application / specific library imports
from ..conf import settings


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

        # take all content
        self.content = self.soup.find_all("body")

        # if we have settings to remove unwanted blocks
        if settings.DJANGO_CHECK_SEO_EXCLUDE_CONTENT != "":
            # iterate through each body (should be only 1)
            for body in self.content:
                # and remove selecte blocks
                for node in body.select(settings.DJANGO_CHECK_SEO_EXCLUDE_CONTENT):
                    node.extract()

        # get content without doublewords thx to custom separator ("<h1>Title</h1><br /><p>Content</p>" -> TitleContent)
        self.content_text = ""
        for c in self.content:
            self.content_text += c.get_text(separator=" ")

        # strip multiple carriage return (with optional space) to only one
        self.content_text = re.sub(r"(\n( ?))+", "\n", self.content_text)
        # strip multiples spaces (>3) to only 2 (for title readability)
        self.content_text = re.sub(r"   +", "  ", self.content_text)

        self.full_url = full_url
        self.keywords = []
        self.problems = []
        self.warnings = []
        self.success = []
