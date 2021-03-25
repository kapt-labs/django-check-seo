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
    <a href="/link1">Heyy !</a>
</html>
"""


class settings:
    def __init__(self):
        self.DJANGO_CHECK_SEO_SETTINGS = {
            "internal_links": 1,
            "external_links": 1,
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
        self.content = self.soup.find_all("body")
        self.full_url = "https://localhost/fake-url/title-of-the-page/"
        # populate class with data
        self.page_stats = site.Site(self.soup, self.full_url)


class patch_get_content_class:
    def __init__(self):
        self.domain = "https://localhost/"


def test_link_importance():
    from django_check_seo.checks_list import check_links

    assert check_links.importance() == 1


def test_links_internal_noexternal(monkeypatch):
    from django.contrib.sites.models import Site
    from django_check_seo.checks_list import check_links

    site = init()
    monkeypatch.setattr(Site.objects, "get_current", patch_get_content_class)
    check_links.run(site)

    for warning in site.warnings:
        if warning.name == "Not enough external links":
            assert warning.name == "Not enough external links"
            assert warning.settings == "at least 1"
            assert warning.found == 0
            assert warning.searched_in == []
            assert (
                warning.description
                == "External links help your users to check your topic and can save them from having to do additional research."
            )

    for success in site.success:
        if success.name == "Internal links were found":
            assert success.name == "Internal links were found"
            assert success.settings == "at least 1"
            assert success.found == 1
            assert success.searched_in == ['<a href="/link1">Heyy !</a>']
            assert (
                success.description
                == "Internal links are useful because they can give the structure of your website to search engines, so they can create a hierarchy of your pages."
            )


def test_links_nointernal_external(monkeypatch):
    from django.contrib.sites.models import Site
    from django_check_seo.checks_list import check_links

    site = init()
    site.soup.find("a")["href"] = "https://github.com/kapt-labs/django-check-seo"
    monkeypatch.setattr(Site.objects, "get_current", patch_get_content_class)
    check_links.run(site)

    for warning in site.warnings:
        if warning.name == "Not enough internal links":
            assert warning.name == "Not enough internal links"
            assert warning.settings == "at least 1"
            assert warning.found == 0
            assert warning.searched_in == []
            assert (
                warning.description
                == "Internal links are useful because they can give the structure of your website to search engines, so they can create a hierarchy of your pages."
            )

    for success in site.success:
        if success.name == "External links were found":
            assert success.name == "External links were found"
            assert success.settings == "at least 1"
            assert success.found == 1
            assert success.searched_in == [
                '<a href="https://github.com/kapt-labs/django-check-seo">Heyy !</a>'
            ]
            assert (
                success.description
                == "External links help your users to check your topic and can save them from having to do additional research."
            )


def test_links_internal_img(monkeypatch):
    from django.contrib.sites.models import Site
    from django_check_seo.checks_list import check_links

    site = init()
    site.soup.find("a").decompose()
    site.soup.body.append(
        (
            BeautifulSoup(
                '<a href="/"><img src="none" alt="Hey!!!" /></a>',
                features="lxml",
            )
        )
    )
    monkeypatch.setattr(Site.objects, "get_current", patch_get_content_class)
    check_links.run(site)

    for success in site.success:
        if success.name == "Internal links were found":
            assert success.name == "Internal links were found"
            assert success.settings == "at least 1"
            assert success.found == 1
            assert success.searched_in == ['<a href="/">Hey!!! (&lt;img&gt;)</a>']


def test_links_internal_img_no_alt_tag(monkeypatch):
    from django.contrib.sites.models import Site
    from django_check_seo.checks_list import check_links

    site = init()
    site.soup.find("a").decompose()
    site.soup.body.append(
        (
            BeautifulSoup(
                '<a href="/"><img src="none" /></a>',
                features="lxml",
            )
        )
    )
    monkeypatch.setattr(Site.objects, "get_current", patch_get_content_class)
    check_links.run(site)

    for success in site.success:
        if success.name == "Internal links were found":
            assert success.name == "Internal links were found"
            assert success.settings == "at least 1"
            assert success.found == 1
            assert success.searched_in == ['<a href="/">&lt;img src="none"/&gt;</a>']


def test_links_internal_empty(monkeypatch):
    from django.contrib.sites.models import Site
    from django_check_seo.checks_list import check_links

    site = init()
    site.soup.find("a").decompose()
    site.soup.body.append(
        (
            BeautifulSoup(
                '<a href="/"></a>',
                features="lxml",
            )
        )
    )
    monkeypatch.setattr(Site.objects, "get_current", patch_get_content_class)
    check_links.run(site)

    for success in site.success:
        if success.name == "Internal links were found":
            assert success.name == "Internal links were found"
            assert success.settings == "at least 1"
            assert success.found == 1
            assert success.searched_in == ['<a href="/">[no content]</a>']
