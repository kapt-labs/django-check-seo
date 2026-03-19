# -*- coding: utf-8 -*-
"""
Resolve Django CMS edit/preview URLs for SEO checks.

When the "page" parameter is a CMS edit or preview URL (e.g. .../cms/placeholder/object/3/edit/372/),
we can resolve it to the public page URL (get_cms_url_for_check_seo) or to the preview URL
(get_preview_url_for_check_seo) so client.get() fetches the right content.
"""

import re
from urllib.parse import urlparse

# Pattern for CMS placeholder edit or preview URL: .../cms/placeholder/object/<object_id>/[edit|preview]/<placeholder_id>/
_CMS_PLACEHOLDER_EDIT_PREVIEW_PATTERN = re.compile(
    r"cms/placeholder/object/(\d+)/(edit|preview)/(\d+)",
    re.IGNORECASE,
)


def _path_from_param(page_param):
    """Return the path part of page_param (strip query string, ensure path)."""
    if not page_param or not page_param.strip():
        return None
    s = page_param.strip()
    if "?" in s:
        s = s.split("?", 1)[0]
    path = urlparse(s).path if s.startswith("/") or "://" in s else s
    if not path.startswith("/"):
        path = "/" + path
    return path


def _path_and_language_from_path(path):
    """
    Split path into (path_without_language, language) for PageUrl lookup.

    PageUrl stores path without the language prefix and language in a separate field.
    - Translated URL (e.g. /en/blog/) → ("/blog/", "en")
    - Non-translated URL (e.g. /blog/) → ("/blog/", "")

    Uses Django's LANGUAGES to detect if the first segment is a language code.
    """
    if not path or path == "/":
        return "/", ""
    segments = [s for s in path.rstrip("/").split("/") if s]
    if not segments:
        return "/", ""
    try:
        from django.conf import settings

        language_codes = [code for code, _ in getattr(settings, "LANGUAGES", [])]
    except Exception:
        language_codes = []
    if language_codes and segments[0] in language_codes:
        language = segments[0]
        rest = segments[1:]
        path_without_lang = "/" + "/".join(rest) if rest else "/"
        return path_without_lang, language
    return path.rstrip("/") or "/", ""


def get_cms_url_for_check_seo(page_param):
    """
    If page_param is a Django CMS edit or preview URL, return the public page path
    by resolving via PageContent and Page.get_absolute_url(). Otherwise return None.

    Returns:
        str: Public path (e.g. /en/blog/) to use for client.get(), or None to use page_param as-is.
    """
    path = _path_from_param(page_param)
    if path is None:
        return None

    from django_check_seo.conf import settings as dcs_settings

    if not getattr(dcs_settings, "DJANGO_CHECK_SEO_CMS_EDIT_URL_TO_PUBLIC", True):
        return None

    match = _CMS_PLACEHOLDER_EDIT_PREVIEW_PATTERN.search(path)
    if not match:
        return None

    object_id = match.group(3)  # .../object/<content_type_id>/edit|preview/<object_id>/
    try:
        from cms.models import PageContent

        content = (
            PageContent.admin_manager.filter(pk=object_id)
            .select_related("page")
            .first()
        )
        if content and content.page_id:
            page = content.page
            public_path = page.get_absolute_url(language=content.language)
            if public_path:
                return public_path if public_path.startswith("/") else "/" + public_path
    except Exception:
        # ImportError when cms is not installed, or RuntimeError etc. when cms is not configured
        pass
    return None


def get_preview_url_for_check_seo(page_param):
    """
    If page_param is a Django CMS edit or preview URL, return the normalized preview path
    (segment edit or preview forced to "preview"). Otherwise return None.

    Returns:
        str: Preview path (e.g. /en/admin/cms/placeholder/object/3/preview/372/) or None.
    """
    path = _path_from_param(page_param)
    if path is None:
        return None

    match = _CMS_PLACEHOLDER_EDIT_PREVIEW_PATTERN.search(path)
    if not match:
        return None

    # Normalize to "preview" (group 2 is the edit|preview segment)
    preview_path = path[: match.start(2)] + "preview" + path[match.end(2) :]
    if "?" in (page_param or ""):
        query = (page_param or "").split("?", 1)[1]
        if query:
            preview_path += "?" + query
    return preview_path if preview_path.startswith("/") else "/" + preview_path


def get_cms_page_id_language(page_param):
    """
    Return (page_id, language) for the given page param (edit/preview URL or public path).

    - If page_param is a Django CMS edit or preview URL, resolve via PageContent
      (object_id is the second number in .../object/<content_type_id>/edit|preview/<object_id>/).
    - Otherwise treat page_param as a public path and resolve via PageUrl when django CMS
      is available (returns (None, None) if not a CMS page or CMS not installed).

    Returns:
        tuple: (page_id, language) or (None, None).
    """
    path = _path_from_param(page_param)
    if path is None:
        return (None, None)

    match = _CMS_PLACEHOLDER_EDIT_PREVIEW_PATTERN.search(path)
    if not match:
        try:
            from cms.models import PageUrl

            path_without_lang, language = _path_and_language_from_path(path)
            page_url = PageUrl.objects.filter(
                path=path_without_lang, language=language or ""
            ).first()
            if not page_url and path_without_lang == "/":
                page_url = PageUrl.objects.filter(
                    path="", language=language or ""
                ).first()
            if page_url:
                return (page_url.page_id, page_url.language or "")
            return (None, None)
        except Exception:
            return (None, None)

    object_id = match.group(3)  # .../object/<content_type_id>/edit|preview/<object_id>/
    try:
        from cms.models import PageContent

        content = PageContent.admin_manager.get(pk=object_id)
        if content and content.page_id:
            return (content.page_id, content.language or "")
    except Exception:
        pass
    return (None, None)
