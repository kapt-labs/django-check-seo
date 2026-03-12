# -*- coding: utf-8 -*-
"""
Keywords discovery functions.

Each function has the signature (site) -> None and must set site.keywords
to a list of strings. Used when DJANGO_CHECK_SEO_KEYWORDS_DISCOVERY_METHOD
points to one of these functions.
"""

from urllib.parse import urlparse

from django_check_seo.models import Page


def meta_keywords(site):
    """Populate site.keywords from the meta name="keywords" content attribute."""
    site.keywords = []
    meta = site.soup.find_all("meta")
    for tag in meta:
        if (
            "name" in tag.attrs
            and tag.attrs["name"] == "keywords"
            and "content" in tag.attrs
            and tag.attrs["content"].strip() != ""
        ):
            site.keywords = list(
                map(str.strip, tag.attrs["content"].strip().split(","))
            )
            break


def model_keywords(site):
    """Populate site.keywords from Page/Keyword models for the current path."""
    site.keywords = []
    path = urlparse(site.full_url).path or "/"
    if not path.startswith("/"):
        path = "/" + path
    try:
        page = Page.objects.get(path=path)
        site.keywords = [kw.name for kw in page.keywords.all()]
    except Page.DoesNotExist:
        pass
