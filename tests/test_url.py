# -*- coding: utf-8 -*-

# Use ./launch_tests.sh to launch these tests.

from bs4 import BeautifulSoup
from django_check_seo.checks import site

html_content = """
<!doctype html>
<html>
    <head>
        <meta name="keywords" content="description,  title">
        <title>Title of the page</title>
    </head>
</html>
"""


class settings:
    def __init__(self):
        self.DJANGO_CHECK_SEO_SETTINGS = {
            "max_link_depth": 4,
            "max_url_length": 70,
        }


class init:
    def __init__(self):
        self.keywords = []
        self.problems = []
        self.warnings = []
        self.success = []
        self.settings = settings()
        self.soup = BeautifulSoup(html_content, features="lxml")
        self.full_url = "https://localhost/fake-url/title-of-the-page/"
        # populate class with data
        self.page_stats = site.Site(self.soup, self.full_url)


def test_url_importance():
    from django_check_seo.checks_list import check_url

    assert check_url.importance() == 1


def test_url_okay():
    from django_check_seo.checks_list import check_url

    site = init()
    check_url.run(site)

    for success in site.success:
        if success.name == "Right amount of level in path":
            assert success.name == "Right amount of level in path"
            assert success.settings == "less than 4"
            assert success.found == 2
            assert success.searched_in == [
                'https://localhost<b><u class="good">/</u></b>fake-url<b><u class="good">/</u></b>title-of-the-page/'
            ]
            assert (
                success.description
                == "Google recommand to organize your content by adding depth in your url, but advises against putting too much depth."
            )

        if success.name == "URL length is great":
            assert success.name == "URL length is great"
            assert success.settings == "less than 70"
            assert success.found == 37
            assert success.searched_in == ["localhost/fake-url/title-of-the-page/"]
            assert (
                success.description
                == "Shorter URLs tend to rank better than long URLs."
            )


def test_url_too_deep():
    from django_check_seo.checks_list import check_url

    site = init()
    site.full_url = "https://localhost/really/too/much/levels/in/path/"
    check_url.run(site)

    for problem in site.problems:
        if problem.name == "Too many levels in path":
            assert problem.name == "Too many levels in path"
            assert problem.settings == "less than 4"
            assert problem.found == 6
            assert problem.searched_in == [
                'https://localhost<b><u>/</u></b>really<b><u>/</u></b>too<b><u>/</u></b>much<b><u>/</u></b>levels<b><u class="problem">/</u></b>in<b><u class="problem">/</u></b>path/'
            ]


def test_url_too_long():
    from django_check_seo.checks_list import check_url

    site = init()
    site.full_url = "https://localhost/this-is-a-veeeeeeery-long-url-which-will-trigger-a-warning-lorem-ipsum/"
    check_url.run(site)

    for warning in site.warnings:
        if warning.name == "URL is too long":
            assert warning.name == "URL is too long"
            assert warning.settings == "less than 70"
            assert warning.found == 81
            assert warning.searched_in == [
                'localhost/this-is-a-veeeeeeery-long-url-which-will-trigger-a-warning-l<b class="problem">orem-ipsum/</b>'
            ]
            assert (
                warning.description
                == "Shorter URLs tend to rank better than long URLs."
            )
