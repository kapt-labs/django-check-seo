# coding: utf-8

# Use ./launch_tests.sh to launch these tests.

from django_check_seo.checks import site
from django_check_seo.checks_list import launch_checks
from bs4 import BeautifulSoup


html_content = """
<!doctype html>
<html>
    <head>
        <title>Home</title>
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <meta name="description" content="Here is the description of the page.">
        <meta name="keywords" content="description,  title">
    </head>
    <body>
        <div class="container">
            <ul class="nav">
                <li class="child selected">
                    <a href="/fr/">Home</a>
                    <ul>
                        <li class="child descendant">
                            <a href="/fr/blog/">Blog</a>
                        </li>
                        <li class="child descendant">
                            <a href="/fr/page-3/">Page 3</a>
                        </li>
                    </ul>
                </li>
                <li class="child sibling">
                    <a href="/fr/page-2/">Page 2</a>
                </li>
            </ul>
            <h1>Title of the page</h1>
            <h2>Subtitle of the page</h2>
            <p>
                Here is the content of the page, without any description.<br />
                <a href="/home/">Internal link</a>.<br />
                <a href="https://github.com/kapt-labs/django-check-seo">External link</a>.
            </p>
        </div>
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

    site = init()

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
