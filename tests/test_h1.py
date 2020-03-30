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
    <body>
        <h1>Title of the page</h1>
    </body>
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


def test_h1_importance():
    from django_check_seo.checks_list import check_h1

    assert check_h1.importance() == 1


def test_h1_1_nokw():
    from django_check_seo.checks_list import check_h1

    site = init()

    check_h1.run(site)

    for success in site.success:
        assert success.name == "H1 tag found"
        assert success.settings == "exactly 1"
        assert success.found == 1
        assert success.searched_in == ["Title of the page"]
        assert (
            success.description
            == "Google is not really concerned about the number of h1 tags on your page, but Bing clearly indicates in its guidelines for webmasters to use only one h1 tag per page."
        )


def test_h1_2_nokw():
    import copy

    from django_check_seo.checks_list import check_h1

    site = init()
    site.soup.body.append(copy.copy(site.soup.find("h1")))

    check_h1.run(site)

    for problem in site.problems:
        if problem.name == "Too much h1 tags":
            assert problem.name == "Too much h1 tags"
            assert problem.settings == "exactly 1"
            assert problem.found == 2
            assert problem.searched_in == ["Title of the page", "Title of the page"]
            assert (
                problem.description
                == "Google is not really concerned about the number of h1 tags on your page, but Bing clearly indicates in its guidelines for webmasters to use only one h1 tag per page."
            )


def test_h1_0_nokw():
    from django_check_seo.checks_list import check_h1

    site = init()
    site.soup.find("h1").decompose()
    check_h1.run(site)

    for problem in site.problems:
        if problem.name == "No h1 tag":
            assert problem.name == "No h1 tag"
            assert problem.settings == "exactly 1"
            assert problem.found == "none"
            assert problem.searched_in == []
            assert (
                problem.description
                == "Google is not really concerned about the number of h1 tags on your page, but Bing clearly indicates in its guidelines for webmasters to use only one h1 tag per page."
            )


def test_h1_1_nokw_image():
    from django_check_seo.checks_list import check_h1

    site = init()
    site.soup.find("h1").decompose()
    site.soup.body.append(
        (
            BeautifulSoup(
                "<h1><img src='none' alt='Title of the page' /></h1>", features="lxml"
            )
        )
    )
    check_h1.run(site)

    for success in site.success:
        assert success.name == "H1 tag found"
        assert success.settings == "exactly 1"
        assert success.found == 1
        assert success.searched_in == ["Title of the page"]
        assert (
            success.description
            == "Google is not really concerned about the number of h1 tags on your page, but Bing clearly indicates in its guidelines for webmasters to use only one h1 tag per page."
        )


def test_h1_1_kw():
    from django_check_seo.checks_list import check_h1
    from django_check_seo.checks_list import check_keywords

    site = init()

    check_keywords.run(site)

    check_h1.run(site)

    for success in site.success:
        if success.name == "Keyword found in h1":
            assert success.name == "Keyword found in h1"
            assert success.settings == "at least one"
            assert success.found == "title"
            assert success.searched_in == ['<b class="good">title</b> of the page']
            assert (
                success.description
                == "The h1 tag represent the main title of your page, and you may populate it with appropriate content in order to ensure that users (and search engines!) will understand correctly your page."
            )


def test_h1_1_kws():
    from django_check_seo.checks_list import check_h1
    from django_check_seo.checks_list import check_keywords

    site = init()
    site.soup.find("h1").string = "Title of the page description"

    check_keywords.run(site)

    check_h1.run(site)

    for success in site.success:
        if success.name == "Keyword found in h1":
            assert success.name == "Keyword found in h1"
            assert success.settings == "at least one"
            assert success.found == "description, title"
            assert success.searched_in == [
                '<b class="good">title</b> of the page <b class="good">description</b>'
            ]
            assert (
                success.description
                == "The h1 tag represent the main title of your page, and you may populate it with appropriate content in order to ensure that users (and search engines!) will understand correctly your page."
            )


def test_h1_1_kw_strange1():
    from django_check_seo.checks_list import check_h1
    from django_check_seo.checks_list import check_keywords

    site = init()
    site.soup.select('meta[name="keywords"]')[0]["content"] = "@letics"

    site.soup.find("h1").string = "word @letics another-word"

    check_keywords.run(site)

    check_h1.run(site)

    for success in site.success:
        if success.name == "Keyword found in h1":
            assert success.found == "@letics"
            assert success.searched_in == [
                'word <b class="good">@letics</b> another-word'
            ]
