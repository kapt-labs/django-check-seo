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
        <h2>Subtitle of the page</h2>
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


def test_h2_importance():
    from django_check_seo.checks_list import check_h2

    assert check_h2.importance() == 1


def test_h2_1_nokw():
    from django_check_seo.checks_list import check_h2

    site = init()

    check_h2.run(site)

    for success in site.success:
        assert success.name == "H2 tags were found"
        assert success.settings == "at least one"
        assert success.found == 1
        assert success.searched_in == ["Subtitle of the page"]
        assert (
            success.description
            == "H2 tags are useful because they are explored by search engines and can help them understand the subject of your page."
        )


def test_h2_2_nokw():
    import copy

    from django_check_seo.checks_list import check_h2

    site = init()
    site.soup.body.append(copy.copy(site.soup.find("h2")))

    check_h2.run(site)

    for success in site.success:
        assert success.name == "H2 tags were found"
        assert success.settings == "at least one"
        assert success.found == 2
        assert success.searched_in == ["Subtitle of the page", "Subtitle of the page"]
        assert (
            success.description
            == "H2 tags are useful because they are explored by search engines and can help them understand the subject of your page."
        )


def test_h2_0_nokw():
    from django_check_seo.checks_list import check_h2

    site = init()
    site.soup.find("h2").decompose()
    check_h2.run(site)

    for warning in site.warnings:
        if warning.name == "No h2 tag":
            assert warning.name == "No h2 tag"
            assert warning.settings == "at least one"
            assert warning.found == "none"
            assert warning.searched_in == []


def test_h2_1_nokw_image():
    from django_check_seo.checks_list import check_h2

    site = init()
    site.soup.find("h2").decompose()
    site.soup.body.append(
        (
            BeautifulSoup(
                "<h2><img src='none' alt='Title of the page' /></h2>", features="lxml"
            )
        )
    )
    check_h2.run(site)

    for success in site.success:
        assert success.name == "H2 tags were found"
        assert success.settings == "at least one"
        assert success.found == 1
        assert success.searched_in == ["Title of the page"]
        assert (
            success.description
            == "H2 tags are useful because they are explored by search engines and can help them understand the subject of your page."
        )


def test_h2_1_kw():
    from django_check_seo.checks_list import check_h2
    from django_check_seo.checks_list import check_keywords

    site = init()

    check_keywords.run(site)
    site.soup.find("h2").string = "Title of the page"

    check_h2.run(site)

    for success in site.success:
        if success.name == "Keyword found in h2 tags":
            assert success.name == "Keyword found in h2 tags"
            assert success.settings == "at least one"
            assert success.found == "title"
            assert success.searched_in == ['<b class="good">title</b> of the page']
            assert (
                success.description
                == "Google uses h2 tags to better understand the subjects of your page."
            )


def test_h2_2_kw():
    import copy
    from django_check_seo.checks_list import check_h2
    from django_check_seo.checks_list import check_keywords

    site = init()

    check_keywords.run(site)
    site.soup.find("h2").string = "Title of the page"
    site.soup.body.append(copy.copy(site.soup.find("h2")))

    check_h2.run(site)

    for success in site.success:
        if success.name == "Keyword found in h2 tags":
            assert success.name == "Keyword found in h2 tags"
            assert success.settings == "at least one"
            assert success.found == "title, title"
            assert success.searched_in == [
                '<b class="good">title</b> of the page',
                '<b class="good">title</b> of the page',
            ]
            assert (
                success.description
                == "Google uses h2 tags to better understand the subjects of your page."
            )


def test_h2_1_kws():
    from django_check_seo.checks_list import check_h2
    from django_check_seo.checks_list import check_keywords

    site = init()

    check_keywords.run(site)
    site.soup.find("h2").string = "Title of the page description"

    check_h2.run(site)

    for success in site.success:
        if success.name == "Keyword found in h2 tags":
            assert success.name == "Keyword found in h2 tags"
            assert success.settings == "at least one"
            assert success.found == "description, title"
            assert success.searched_in == [
                '<b class="good">title</b> of the page <b class="good">description</b>'
            ]


def test_h2_2_kws():
    import copy
    from django_check_seo.checks_list import check_h2
    from django_check_seo.checks_list import check_keywords

    site = init()

    check_keywords.run(site)
    site.soup.body.append(copy.copy(site.soup.find("h2")))
    site.soup.find("h2").string = "Title of the page description"

    check_h2.run(site)

    for success in site.success:
        if success.name == "Keyword found in h2 tags":
            assert success.name == "Keyword found in h2 tags"
            assert success.settings == "at least one"
            assert success.found == "description, title"
            assert success.searched_in == [
                '<b class="good">title</b> of the page <b class="good">description</b>',
                "subtitle of the page",
            ]
