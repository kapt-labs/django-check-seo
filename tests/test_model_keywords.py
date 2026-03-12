# Tests for model_keywords discovery (require DB)

import pytest
from bs4 import BeautifulSoup

from django_check_seo.models import Keyword, Page
from django_check_seo.utils.keywords_discovery import model_keywords

html_content = """
<!doctype html>
<html><head></head><body></body></html>
"""


def _make_site(path="/fr/ma-page/"):
    obj = type("Site", (), {})()
    obj.keywords = []
    obj.soup = BeautifulSoup(html_content, features="lxml")
    obj.full_url = "https://example.com" + path
    return obj


@pytest.mark.django_db
def test_model_keywords_found():
    """model_keywords sets site.keywords from Page/Keyword for matching path."""
    kw1 = Keyword.objects.create(name="foo")
    kw2 = Keyword.objects.create(name="bar")
    p = Page.objects.create(path="/fr/ma-page/")
    p.keywords.add(kw1, kw2)

    site_obj = _make_site("/fr/ma-page/")
    model_keywords(site_obj)
    assert site_obj.keywords == ["foo", "bar"]


@pytest.mark.django_db
def test_model_keywords_unknown_path():
    """model_keywords leaves site.keywords empty when no Page for path."""
    site_obj = _make_site("/unknown/path/")
    model_keywords(site_obj)
    assert site_obj.keywords == []


@pytest.mark.django_db
def test_model_keywords_empty_page():
    """model_keywords sets site.keywords to [] when Page has no keywords."""
    Page.objects.create(path="/fr/empty/")
    site_obj = _make_site("/fr/empty/")
    model_keywords(site_obj)
    assert site_obj.keywords == []


@pytest.mark.django_db
def test_model_keywords_path_with_leading_slash():
    """Path from URL is used as-is when it starts with /."""
    kw = Keyword.objects.create(name="baz")
    p = Page.objects.create(path="/no-leading-slash")
    p.keywords.add(kw)

    site_obj = _make_site("/no-leading-slash")
    model_keywords(site_obj)
    assert site_obj.keywords == ["baz"]
