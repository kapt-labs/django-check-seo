from bs4 import BeautifulSoup

from django_check_seo.checks import site
from django_check_seo.utils.keywords_discovery import meta_keywords

# Use ./launch_tests.sh to launch these tests.


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


def test_keyword_url_importance():
    from django_check_seo.checks_list import check_keyword_url

    assert check_keyword_url.importance() == 1


def test_keyword_url_kw():
    from django_check_seo.checks_list import check_keyword_url, check_keywords

    site = init()

    meta_keywords(site)
    check_keywords.run(site)
    check_keyword_url.run(site)

    for success in site.success:
        if success.name == "Keywords found in URL":
            assert success.name == "Keywords found in URL"
            assert success.settings == "at least one"
            assert success.found == "title"
            assert success.searched_in == [
                'https://localhost/fake-url/<b class="good">title</b>-of-the-page/'
            ]
            assert (
                success.description
                == 'Keywords in URL will help your users understand the organisation of your website, and are a small ranking factor for Google. On the other hand, Bing guidelines advises to "<i>keep [your URL] clean and keyword rich when possible</i>".<br />Warning, Django Check SEO will try to find keywords in the URL without apostrophes ("pour-lenergie" will be found, but not "pour-l-energie").'
            )


def test_keyword_url_nokw():
    from django_check_seo.checks_list import check_keyword_url, check_keywords

    site = init()
    meta_keywords(site)
    check_keywords.run(site)
    site.full_url = "https://localhost/fake-url/notitle-of-the-page"
    check_keyword_url.run(site)

    for problem in site.problems:
        if problem.name == "No keyword in URL":
            assert problem.name == "No keyword in URL"
            assert problem.settings == "at least one"
            assert problem.found == "none"
            assert problem.searched_in == [
                "https://localhost/fake-url/notitle-of-the-page"
            ]


def test_keyword_url_nokw_root():
    from django_check_seo.checks_list import check_keyword_url, check_keywords

    site = init()
    meta_keywords(site)
    check_keywords.run(site)
    site.full_url = "https://localhost/"
    check_keyword_url.run(site)

    for success in site.success:
        if success.name == "Keywords found in URL":
            raise ValueError("We don't espect kw to be found in root URL")

    for problem in site.problems:
        if problem.name == "No keyword in URL":
            raise ValueError(
                "We shouldnt return a problem if a keyword is not found in root URL"
            )


def test_keyword_url_kws():
    from django_check_seo.checks_list import check_keyword_url, check_keywords

    site = init()
    site.soup.select('meta[name="keywords"]')[0]["content"] = "title,  page"

    meta_keywords(site)
    check_keywords.run(site)
    site.full_url = "https://localhost/fake-url/title-of-the-page"

    check_keyword_url.run(site)

    for success in site.success:
        if success.name == "Keywords found in URL":
            assert success.name == "Keywords found in URL"
            assert success.settings == "at least one"
            assert success.found == "title, page"
            assert success.searched_in == [
                'https://localhost/fake-url/<b class="good">title</b>-of-the-<b class="good">page</b>'
            ]


def test_keyword_url_kw_accented():
    from django_check_seo.checks_list import check_keyword_url, check_keywords

    site = init()
    site.soup.select('meta[name="keywords"]')[0]["content"] = "énergie"

    meta_keywords(site)
    check_keywords.run(site)
    site.full_url = "https://localhost/fake-url/title-of-energie"

    check_keyword_url.run(site)

    for success in site.success:
        if success.name == "Keywords found in URL":
            assert success.name == "Keywords found in URL"
            assert success.settings == "at least one"
            assert success.found == "énergie"
            assert success.searched_in == [
                'https://localhost/fake-url/title-of-<b class="good">energie</b>'
            ]


def test_keyword_url_kws_accented():
    from django_check_seo.checks_list import check_keyword_url, check_keywords

    site = init()
    site.soup.select('meta[name="keywords"]')[0]["content"] = "énergie,  éééé"

    meta_keywords(site)
    check_keywords.run(site)
    site.full_url = "https://localhost/fake-url/title-eeee-energie"

    check_keyword_url.run(site)

    for success in site.success:
        if success.name == "Keywords found in URL":
            assert success.name == "Keywords found in URL"
            assert success.settings == "at least one"
            assert success.found == "énergie, éééé"
            assert success.searched_in == [
                'https://localhost/fake-url/title-<b class="good">eeee</b>-<b class="good">energie</b>'
            ]


def test_keyword_url_kws_accented_unaccented():
    from django_check_seo.checks_list import check_keyword_url, check_keywords

    site = init()
    site.soup.select('meta[name="keywords"]')[0]["content"] = "énergie,  title"

    meta_keywords(site)
    check_keywords.run(site)
    site.full_url = "https://localhost/fake-url/title-of-energie"

    check_keyword_url.run(site)

    for success in site.success:
        if success.name == "Keywords found in URL":
            assert success.name == "Keywords found in URL"
            assert success.settings == "at least one"
            assert success.found == "énergie, title"
            assert success.searched_in == [
                'https://localhost/fake-url/<b class="good">title</b>-of-<b class="good">energie</b>'
            ]
