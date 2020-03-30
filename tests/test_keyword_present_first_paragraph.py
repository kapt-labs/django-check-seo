# -*- coding: utf-8 -*-

# Use ./launch_tests.sh to launch these tests.

import re

from bs4 import BeautifulSoup
from django_check_seo.checks import site

html_content = """
<!doctype html>
<html>
    <head>
        <meta name="keywords" content="description,  title">
        <title>Title of the page</title>
    </head>
    <body><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi pharetra metus ut tellus interdum consectetur. In vehicula orci vel fermentum pretium. Vestibulum ante ipsum primis in faucibus orci title luctus et ultrices posuere cubilia Curae; Cras consequat nunc arcu, ut tristique nulla molestie vel. Morbi vitae diam nibh. Proin ex nutella.</p></body>
</html>
"""


class settings:
    def __init__(self):
        self.DJANGO_CHECK_SEO_SETTINGS = {
            "keywords_in_first_words": 50,
        }


class init:
    def __init__(self):
        self.keywords = []
        self.problems = []
        self.warnings = []
        self.success = []
        self.settings = settings()
        self.soup = BeautifulSoup(html_content, features="lxml")

        self.content_text = get_content_text(self.soup.find_all("body"))

        self.full_url = "https://localhost/fake-url/title-of-the-page/"
        # populate class with data
        self.page_stats = site.Site(self.soup, self.full_url)


def get_content_text(soup):
    content_text = ""
    for c in soup:
        content_text += c.get_text(separator=" ")

    # strip multiple carriage return (with optional space) to only one
    content_text = re.sub(r"(\n( ?))+", "\n", content_text)
    # strip multiples spaces (>3) to only 2 (for title readability)
    content_text = re.sub(r"   +", "  ", content_text)
    return content_text


def test_url_importance():
    from django_check_seo.checks_list import keyword_present_first_paragraph

    assert keyword_present_first_paragraph.importance() == 1


def test_keyword_present_first_paragraph_kw():
    from django_check_seo.checks_list import check_keywords
    from django_check_seo.checks_list import keyword_present_first_paragraph

    site = init()
    check_keywords.run(site)
    keyword_present_first_paragraph.run(site)

    for success in site.success:
        if success.name == "Keywords found in first paragraph":
            assert success.name == "Keywords found in first paragraph"
            assert success.settings == "before 50 words"
            assert success.found == "title"
            assert success.searched_in == [
                'lorem ipsum dolor sit amet, consectetur adipiscing elit. morbi pharetra metus ut tellus interdum consectetur. in vehicula orci vel fermentum pretium. vestibulum ante ipsum primis in faucibus orci <b class="good">title</b> luctus et ultrices posuere cubilia curae; cras consequat nunc arcu, ut tristique nulla molestie vel. morbi vitae diam nibh. proin ex'
            ]
            assert (
                success.description
                == "The reader will be relieved to find one of his keywords in the first paragraph of your page, and the same logic applies to Google, which will consider the content more relevant."
            )


def test_keyword_present_first_paragraph_nokw():
    from django_check_seo.checks_list import check_keywords
    from django_check_seo.checks_list import keyword_present_first_paragraph

    site = init()
    site.soup.find("p").string = "There is no keyword inside first 50 words."
    site.content_text = get_content_text(site.soup.find_all("body"))

    check_keywords.run(site)
    keyword_present_first_paragraph.run(site)

    for problem in site.problems:
        if problem.name == "No keyword in first paragraph":
            assert problem.name == "No keyword in first paragraph"
            assert problem.settings == "before 50 words"
            assert problem.found == "none"
            assert problem.searched_in == ["there is no keyword inside first 50 words."]


def test_keyword_present_first_paragraph_kws():
    from django_check_seo.checks_list import check_keywords
    from django_check_seo.checks_list import keyword_present_first_paragraph

    site = init()
    site.soup.find(
        "p"
    ).string = "There are two kw inside the first paragraph: title and description."
    site.content_text = get_content_text(site.soup.find_all("body"))

    check_keywords.run(site)
    keyword_present_first_paragraph.run(site)

    for success in site.success:
        if success.name == "Keywords found in first paragraph":
            assert success.name == "Keywords found in first paragraph"
            assert success.settings == "before 50 words"
            assert success.found == "description, title"
            assert success.searched_in == [
                'there are two kw inside the first paragraph: <b class="good">title</b> and <b class="good">description</b>.'
            ]
            assert (
                success.description
                == "The reader will be relieved to find one of his keywords in the first paragraph of your page, and the same logic applies to Google, which will consider the content more relevant."
            )
