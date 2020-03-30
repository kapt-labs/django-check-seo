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
            "meta_title_length": [30, 60],
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


def test_title_importance():
    from django_check_seo.checks_list import check_title

    assert check_title.importance() == 1


def test_title_notitle():
    from django_check_seo.checks_list import check_title

    site = init()
    site.soup.find("title").decompose()
    check_title.run(site)

    for problem in site.problems:
        if problem.name == "No meta title tag":
            assert problem.name == "No meta title tag"
            assert problem.settings == "one"
            assert problem.found == "none"
            assert problem.searched_in == []
            assert (
                problem.description
                == "Titles tags are ones of the most important things to add to your pages, sinces they are the main text displayed on result search pages."
            )


def test_title_short():
    from django_check_seo.checks_list import check_title

    site = init()
    check_title.run(site)

    for problem in site.problems:
        if problem.name == "Meta title tag is too short":
            assert problem.name == "Meta title tag is too short"
            assert problem.settings == "more than 30"
            assert problem.found == 17
            assert problem.searched_in == ["Title of the page"]
            assert (
                problem.description
                == "Meta titles tags need to describe the content of the page, and need to contain at least a few words."
            )


def test_title_long():
    from django_check_seo.checks_list import check_title

    site = init()
    site.soup.find(
        "title"
    ).string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam pretium in quam sit amet egestas. Nullam cursus mi eu mauris congue laoreet."
    check_title.run(site)

    for warning in site.warnings:
        if warning.name == "Meta title tag is too long":
            assert warning.name == "Meta title tag is too long"
            assert warning.settings == "less than 60"
            assert warning.found == 139
            assert warning.searched_in == [
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Eti<b class="problem">am pretium in quam sit amet egestas. Nullam cursus mi eu mauris congue laoreet.</b>'
            ]
            assert (
                warning.description
                == "Only the first ~55-60 chars are displayed on modern search engines results. Writing a longer meta title is not really required and can lead to make the user miss informations."
            )


def test_title_okay():
    from django_check_seo.checks_list import check_title

    site = init()
    site.soup.find("title").string = "This is a title with a good length."
    check_title.run(site)

    for success in site.success:
        if success.name == "Meta title tag have a good length":
            assert success.name == "Meta title tag have a good length"
            assert success.settings == "more than 30"
            assert success.found == 35
            assert success.searched_in == [
                'This is a title with a good le<b class="good">ngth.</b>'
            ]
            assert (
                success.description
                == "Meta titles tags need to describe the content of the page."
            )


def test_titles():
    import copy
    from django_check_seo.checks_list import check_title

    site = init()
    site.soup.head.append(copy.copy(site.soup.find("title")))
    check_title.run(site)

    for problem in site.problems:
        if problem.name == "Too much meta title tags":
            assert problem.name == "Too much meta title tags"
            assert problem.settings == "only one"
            assert problem.found == 2
            assert problem.searched_in == ["Title of the page", "Title of the page"]
            assert (
                problem.description
                == "Only the first meta title tag will be displayed on the tab space on your browser, and only one meta title tag will be displayed on the search results pages."
            )


def test_title_nokw():
    from django_check_seo.checks_list import check_title
    from django_check_seo.checks_list import check_keywords

    site = init()
    check_keywords.run(site)

    site.soup.find("title").string = "There is notitle on this page."
    check_title.run(site)

    for problem in site.problems:
        if problem.name == "Meta title tag do not contain any keyword":
            assert problem.name == "Meta title tag do not contain any keyword"
            assert problem.settings == "at least one"
            assert problem.found == "none"
            assert problem.searched_in == ["there is notitle on this page."]
            assert (
                problem.description
                == "Meta titles tags need to contain at least one keyword, since they are one of the most important content of the page for search engines."
            )


def test_title_kw():
    from django_check_seo.checks_list import check_title
    from django_check_seo.checks_list import check_keywords

    site = init()
    check_keywords.run(site)

    check_title.run(site)

    for success in site.success:
        if success.name == "Keywords found in meta title tag":
            assert success.name == "Keywords found in meta title tag"
            assert success.settings == "at least one"
            assert success.found == "title"
            assert success.searched_in == ['<b class="good">title</b> of the page']
            assert (
                success.description
                == "Meta titles tags need to contain at least one keyword, since they are one of the most important content of the page for search engines."
            )


def test_title_kws():
    from django_check_seo.checks_list import check_title
    from django_check_seo.checks_list import check_keywords

    site = init()
    check_keywords.run(site)

    site.soup.find("title").string = "This title have a description."
    check_title.run(site)

    for success in site.success:
        if success.name == "Keywords found in meta title tag":
            assert success.name == "Keywords found in meta title tag"
            assert success.settings == "at least one"
            assert success.found == "description, title"
            assert success.searched_in == [
                'this <b class="good">title</b> have a <b class="good">description</b>.'
            ]
