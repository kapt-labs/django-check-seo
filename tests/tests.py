# Use ./launch_tests.sh to launch these tests.
#
#
#       ████████╗███████╗███████╗████████╗███████╗
#       ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝
#          ██║   █████╗  ███████╗   ██║   ███████╗
#          ██║   ██╔══╝  ╚════██║   ██║   ╚════██║
#          ██║   ███████╗███████║   ██║   ███████║
#          ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝

from django_check_seo.checks import site
from django_check_seo.checks_list import launch_checks
from bs4 import BeautifulSoup


html1 = """
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

def test_init():
        soup = BeautifulSoup(html1, features="lxml")
        full_url = "https://localhost/fake-url/title-of-the-page/"
        # populate class with data
        page_stats = site.Site(soup, full_url)

