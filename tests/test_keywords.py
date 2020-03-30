# -*- coding: utf-8 -*-

# Use ./launch_tests.sh to launch these tests.

from bs4 import BeautifulSoup
from django_check_seo.checks import site

html_content = """
<!doctype html>
<html>
    <head>
        <meta name="keywords" content="description,  title">
    </head>
</html>
"""


class init:
    def __init__(self):
        self.keywords = []
        self.problems = []
        self.warnings = []
        self.success = []

        self.soup = BeautifulSoup(html_content, features="lxml")
        self.full_url = "https://localhost/fake-url/title-of-the-page/"
        # populate class with data
        self.page_stats = site.Site(self.soup, self.full_url)


def test_keyword_importance():
    from django_check_seo.checks_list import check_keywords

    assert check_keywords.importance() == 5


def test_keyword_kw():
    from django_check_seo.checks_list import check_keywords

    site = init()

    check_keywords.run(site)

    for success in site.success:
        if success.name == "Keywords found in meta keywords field":
            assert success.name == "Keywords found in meta keywords field"
            assert success.settings == "at least one"
            assert success.found == 2
            assert success.searched_in == ["description", "title"]
            assert (
                success.description
                == "Django-check-seo uses the keywords in the meta keywords field to check all other tests related to the keywords. A series of problems and warnings are related to keywords, and will therefore systematically be activated if the keywords are not filled in."
            )


def test_keyword_nokw():
    from django_check_seo.checks_list import check_keywords

    site = init()
    site.soup.select('meta[name="keywords"]')[0]["content"] = ""

    check_keywords.run(site)

    for problem in site.problems:
        if problem.name == "No keywords in meta keywords field":
            assert problem.name == "No keywords in meta keywords field"
            assert problem.settings == "at least one"
            assert problem.found == "none"
            assert problem.searched_in == []
            assert (
                problem.description
                == "Django-check-seo uses the keywords in the meta keywords field to check all other tests related to the keywords. A series of problems and warnings are related to keywords, and will therefore systematically be activated if the keywords are not filled in."
            )
