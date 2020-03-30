# coding: utf-8

# Use ./launch_tests.sh to launch these tests.

from bs4 import BeautifulSoup
from django_check_seo.checks import site

html_content = """
<!doctype html>
<html>
    <body>
        <img src="none" alt="heyy" />
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
        self.content = self.soup.find_all("body")
        self.full_url = "https://localhost/fake-url/title-of-the-page/"
        # populate class with data
        self.page_stats = site.Site(self.soup, self.full_url)


def test_images_importance():
    from django_check_seo.checks_list import check_images

    assert check_images.importance() == 1


def test_image_okay():
    from django_check_seo.checks_list import check_images

    site = init()

    check_images.run(site)

    for success in site.success:
        if success.name == "Img have alt tag":
            assert success.name == "Img have alt tag"
            assert success.settings == "all images"
            assert success.found == 1
            assert success.searched_in == [
                '<a target="_blank" href="none">image</a> (heyy)'
            ]
            assert (
                success.description
                == 'Your images should always have an alt tag, because it improves accessibility for visually impaired people. The name of the file is important too, because it helps Google understand what your image is about. For example, you could rename a file named "IMG0001.jpg" to "tree_with_a_bird.jpg".'
            )


def test_images_okay():
    import copy
    from django_check_seo.checks_list import check_images

    site = init()

    site.soup.body.append(copy.copy(site.soup.find("img")))
    check_images.run(site)

    for success in site.success:
        if success.name == "Img have alt tag":
            assert success.name == "Img have alt tag"
            assert success.settings == "all images"
            assert success.found == 2
            assert success.searched_in == [
                '<a target="_blank" href="none">image</a> (heyy)',
                '<a target="_blank" href="none">image</a> (heyy)',
            ]
            assert (
                success.description
                == 'Your images should always have an alt tag, because it improves accessibility for visually impaired people. The name of the file is important too, because it helps Google understand what your image is about. For example, you could rename a file named "IMG0001.jpg" to "tree_with_a_bird.jpg".'
            )


def test_image_missing():
    from django_check_seo.checks_list import check_images

    site = init()
    check_images.run(site)

    for problem in site.problems:
        if problem.name == "Img lack alt tag":
            assert problem.name == "Img lack alt tag"
            assert problem.settings == "all images"
            assert problem.found == 1
            assert problem.searched_in == [
                '<b><u class="problem"><a target="_blank" href="none">image</a></u></b>'
            ]


def test_images_missing():
    import copy
    from django_check_seo.checks_list import check_images

    site = init()
    site.soup.find("img")["alt"] = ""
    site.soup.body.append(copy.copy(site.soup.find("img")))
    check_images.run(site)

    for problem in site.problems:
        if problem.name == "Img lack alt tag":
            assert problem.name == "Img lack alt tag"
            assert problem.settings == "all images"
            assert problem.found == 2
            assert problem.searched_in == [
                '<b><u class="problem"><a target="_blank" href="none">image</a></u></b>',
                '<b><u class="problem"><a target="_blank" href="none">image</a></u></b>',
            ]


def test_image_unknown():
    from django_check_seo.checks_list import check_images

    site = init()
    site.soup.find("img")["src"] = ""
    site.soup.find("img")["alt"] = ""
    check_images.run(site)

    for problem in site.problems:
        if problem.name == "Img lack alt tag":
            assert problem.name == "Img lack alt tag"
            assert problem.settings == "all images"
            assert problem.found == 1
            assert problem.searched_in == [
                "<b><u>unknown image</u></b>",
            ]
