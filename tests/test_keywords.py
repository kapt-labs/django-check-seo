# Use ./launch_tests.sh to launch these tests.

from bs4 import BeautifulSoup

from django_check_seo.checks import site
from django_check_seo.utils.keywords_discovery import meta_keywords

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

    site_obj = init()
    meta_keywords(site_obj)
    check_keywords.run(site_obj)

    for success in site_obj.success:
        if success.name == "Keywords found":
            assert success.name == "Keywords found"
            assert success.settings == "at least one"
            assert success.found == 2
            assert success.searched_in == ["description", "title"]
            assert "Django-check-seo uses the keywords" in success.description
            return
    assert False, "Expected 'Keywords found' in success"


def test_keyword_nokw():
    from django_check_seo.checks_list import check_keywords

    site_obj = init()
    site_obj.soup.select('meta[name="keywords"]')[0]["content"] = ""
    meta_keywords(site_obj)
    check_keywords.run(site_obj)

    for problem in site_obj.problems:
        if problem.name == "No keywords defined for this page":
            assert problem.name == "No keywords defined for this page"
            assert problem.settings == "at least one"
            assert problem.found == "none"
            assert problem.searched_in == []
            assert "Django-check-seo uses the keywords" in problem.description
            return
    assert False, "Expected 'No keywords defined for this page' in problems"


def test_meta_keywords_discovery():
    """meta_keywords(site) populates site.keywords from meta tag."""
    site_obj = init()
    assert site_obj.keywords == []
    meta_keywords(site_obj)
    assert site_obj.keywords == ["description", "title"]


def test_meta_keywords_discovery_empty():
    """meta_keywords leaves site.keywords empty when meta is missing or empty."""
    site_obj = init()
    site_obj.soup.select('meta[name="keywords"]')[0]["content"] = ""
    meta_keywords(site_obj)
    assert site_obj.keywords == []
