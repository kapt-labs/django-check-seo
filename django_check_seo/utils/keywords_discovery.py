# -*- coding: utf-8 -*-
"""
Keywords discovery functions.

Each function has the signature (site) -> None and must set site.keywords
to a list of strings. Used when DJANGO_CHECK_SEO_KEYWORDS_DISCOVERY_METHOD
points to one of these functions.
"""

from urllib.parse import urlparse

from django_check_seo.models import Page
from django_check_seo.utils.cms_url_resolution import _path_and_language_from_path


def _normalize_path(path):
    """Ensure path starts with / for lookup."""
    path = path or "/"
    if not path.startswith("/"):
        path = "/" + path
    return path


def get_cms_page_id_language_for_path(path):
    """
    Resolve path to (cms_page_id, language) via Django CMS PageUrl if available.

    PageUrl is looked up by path (without language prefix) and language, so the
    path is split using the same logic as get_cms_page_id_language (translated
    vs non-translated URLs).

    Returns (page_id, language) or (None, None) when not a CMS page (e.g. apphook)
    or when django CMS is not installed.
    """
    path = _normalize_path(path)
    try:
        from cms.models import PageUrl

        path_without_lang, language = _path_and_language_from_path(path)
        page_url = (
            PageUrl.objects.filter(path=path_without_lang, language=language or "")
            .values_list("page_id", "language")
            .first()
        )
        if not page_url and path_without_lang == "/":
            page_url = (
                PageUrl.objects.filter(path="", language=language or "")
                .values_list("page_id", "language")
                .first()
            )
        if page_url:
            return (page_url[0], page_url[1] or "")
        return (None, None)
    except Exception:
        # ImportError when cms is not installed; RuntimeError etc. when cms is not in INSTALLED_APPS
        return (None, None)


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
    path = _normalize_path(path)
    try:
        page = Page.objects.get(path=path)
        site.keywords = [kw.name for kw in page.keywords.all()]
    except Page.DoesNotExist:
        pass


def django_cms_model_keywords(site):
    """
    Populate site.keywords from Page/Keyword models, using (cms_page_id, language)
    when the path resolves to a Django CMS page, else fallback to path (apphooks).

    When site has cms_page_id (and optionally cms_language) set (e.g. in draft
    mode with an edit/preview URL), use them directly so the same keywords are
    used as for the published page.
    """
    site.keywords = []
    cms_page_id = getattr(site, "cms_page_id", None)
    language = getattr(site, "cms_language", None)
    if cms_page_id is not None:
        page = Page.objects.filter(
            cms_page_id=cms_page_id, language=language or ""
        ).first()
        if page:
            site.keywords = [kw.name for kw in page.keywords.all()]
        return

    path = urlparse(site.full_url).path or "/"
    path = _normalize_path(path)

    cms_page_id, language = get_cms_page_id_language_for_path(path)
    if cms_page_id is not None:
        page = Page.objects.filter(cms_page_id=cms_page_id, language=language).first()
        if page:
            site.keywords = [kw.name for kw in page.keywords.all()]
            return

    # Fallback: path-only (e.g. apphook or non-CMS)
    try:
        page = Page.objects.get(path=path)
        site.keywords = [kw.name for kw in page.keywords.all()]
    except Page.DoesNotExist:
        pass
