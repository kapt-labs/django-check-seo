# coding: utf-8

# Use ./launch_tests.sh to launch these tests.

from bs4 import BeautifulSoup
from django_check_seo.checks import site

html_content = """
<!doctype html>
<html>
    <head>
        <meta name="description" content="Here is the description of the page.">
        <meta name="keywords" content="description,  title">
    </head>
    <body>
    </body>
</html>
"""


class settings:
    def __init__(self):
        self.DJANGO_CHECK_SEO_SETTINGS = {"meta_description_length": [50, 160]}


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


def test_decription_importance():
    from django_check_seo.checks_list import check_description

    assert check_description.importance() == 1


def test_description_1_nokw():
    from django_check_seo.checks_list import check_description

    site = init()

    check_description.run(site)

    for success in site.success:
        if success.name == "Meta description is present":
            assert success.name == "Meta description is present"
            assert success.settings == "needed"
            assert success.found == "one"
            assert success.searched_in == ["Here is the description of the page."]
            assert (
                success.description
                == "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
            )
        elif success.name == "Only one meta description tag":
            assert success.name == "Only one meta description tag"
            assert success.settings == "only one"
            assert success.found == "one"
            assert success.searched_in == ["Here is the description of the page."]
            assert (
                success.description
                == "Although some people write one meta description by targeted keyword, this is still an uncommon practice that is not yet recognized by all search engines."
            )


def test_description_1_nokw_too_short_1():
    from django_check_seo.checks_list import check_description

    site = init()

    site.soup.select('meta[name="description"]')[0]["content"] = "a"
    check_description.run(site)

    for problem in site.problems:
        if problem.name == "Meta description is too short":
            assert problem.name == "Meta description is too short"
            assert problem.settings == "between 50 and 160 chars "
            assert problem.found == "1 char"
            assert problem.searched_in == ["a"]


def test_description_1_nokw_too_short_49():
    from django_check_seo.checks_list import check_description

    site = init()

    site.soup.select('meta[name="description"]')[0][
        "content"
    ] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    check_description.run(site)

    for problem in site.problems:
        if problem.name == "Meta description is too short":
            assert problem.name == "Meta description is too short"
            assert problem.settings == "between 50 and 160 chars "
            assert problem.found == "49 chars"
            assert problem.searched_in == [
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            ]


def test_description_1_nokw_too_long_160():
    from django_check_seo.checks_list import check_description

    site = init()

    site.soup.select('meta[name="description"]')[0][
        "content"
    ] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    check_description.run(site)

    for problem in site.problems:
        if problem.name == "Meta description is present":
            assert problem.settings == "between 50 and 160 chars "
            assert problem.found == "160 chars"
            assert problem.searched_in == [
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            ]


def test_description_1_nokw_too_long_161():
    from django_check_seo.checks_list import check_description

    site = init()

    site.soup.select('meta[name="description"]')[0][
        "content"
    ] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"
    check_description.run(site)

    for problem in site.problems:
        if problem.name == "Meta description is present":
            assert problem.settings == "between 50 and 160 chars "
            assert problem.found == "161 chars"
            assert problem.searched_in == [
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"
            ]


def test_description_1_kw():
    from django_check_seo.checks_list import check_keywords
    from django_check_seo.checks_list import check_description

    site = init()

    site.soup.select('meta[name="description"]')[0][
        "content"
    ] = "Here is the description of the page."

    check_keywords.run(site)
    check_description.run(site)

    for success in site.success:
        if success.name == "Keywords were found in meta description":
            assert success.settings == "at least one"
            assert success.found == "description"
            assert success.searched_in == [
                'here is the <b class="good">description</b> of the page.'
            ]


def test_description_1_kws():
    from django_check_seo.checks_list import check_keywords
    from django_check_seo.checks_list import check_description

    site = init()

    site.soup.select('meta[name="description"]')[0][
        "content"
    ] = "Here is the description of the page without title."

    check_keywords.run(site)
    check_description.run(site)

    for success in site.success:
        if success.name == "Keywords were found in meta description":
            assert success.settings == "at least one"
            assert success.found == "description, title"
            assert success.searched_in == [
                'here is the <b class="good">description</b> of the page without <b class="good">title</b>.'
            ]


def test_description_1_length():
    from django_check_seo.checks_list import check_description

    site = init()

    site.soup.select('meta[name="description"]')[0][
        "content"
    ] = "Here is the description of the page without title."
    check_description.run(site)

    for success in site.success:
        if success.name == "Meta description length is correct":
            assert success.name == "Meta description length is correct"
            assert success.settings == "between 50 and 160 chars "
            assert success.found == "50"
            assert success.searched_in == [
                "Here is the description of the page without title."
            ]
            assert (
                success.description
                == "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
            )


def test_description_2():
    import copy
    from django_check_seo.checks_list import check_description

    site = init()

    site.soup.body.append(copy.copy(site.soup.select('meta[name="description"]')[0]))
    check_description.run(site)

    for warning in site.warnings:
        if warning.name == "Too much meta description tags":
            assert warning.name == "Too much meta description tags"
            assert warning.settings == "only one"
            assert warning.found == 2
            assert warning.searched_in == [
                "Here is the description of the page.",
                "Here is the description of the page.",
            ]
            assert (
                warning.description
                == "Although some people write one meta description by targeted keyword, this is still an uncommon practice that is not yet recognized by all search engines."
            )


def test_description_0():
    from django_check_seo.checks_list import check_description

    site = init()

    site.soup.select('meta[name="description"]')[0].decompose()
    check_description.run(site)

    for problem in site.problems:
        if problem.name == "No meta description":
            assert problem.name == "No meta description"
            assert problem.settings == "needed"
            assert problem.found == "none"
            assert problem.searched_in == []
            assert (
                problem.description
                == "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
            )
