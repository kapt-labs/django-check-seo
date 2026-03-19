# Tests for CMS edit/preview URL resolution (no django-cms required for these tests)


from django_check_seo.utils.cms_url_resolution import (
    get_cms_url_for_check_seo,
    get_preview_url_for_check_seo,
)

# --- get_cms_url_for_check_seo ---


def test_get_cms_url_normal_path_returns_none():
    """Normal path is not rewritten."""
    assert get_cms_url_for_check_seo("/fr/ma-page/") is None
    assert get_cms_url_for_check_seo("/") is None


def test_get_cms_url_edit_pattern_without_cms_returns_none():
    """Edit URL pattern without django-cms installed returns None (no resolution)."""
    url = "/en/admin/cms/placeholder/object/3/edit/372/"
    # Without cms.models.PageContent, resolution fails and returns None
    assert get_cms_url_for_check_seo(url) is None


# --- get_preview_url_for_check_seo ---


def test_get_preview_url_edit_returns_preview_path():
    """Edit URL is normalized to preview path."""
    url = "/en/admin/cms/placeholder/object/3/edit/372/"
    assert (
        get_preview_url_for_check_seo(url)
        == "/en/admin/cms/placeholder/object/3/preview/372/"
    )


def test_get_preview_url_edit_with_query_preserves_query():
    """Edit URL with query string preserves it."""
    url = "/en/admin/cms/placeholder/object/3/edit/372/?live-url=/en/blog/"
    assert (
        get_preview_url_for_check_seo(url)
        == "/en/admin/cms/placeholder/object/3/preview/372/?live-url=/en/blog/"
    )


def test_get_preview_url_already_preview_unchanged():
    """Preview URL is returned unchanged (already preview)."""
    url = "/en/admin/cms/placeholder/object/3/preview/372/"
    assert (
        get_preview_url_for_check_seo(url)
        == "/en/admin/cms/placeholder/object/3/preview/372/"
    )


def test_get_preview_url_normal_path_returns_none():
    """Normal path returns None."""
    assert get_preview_url_for_check_seo("/fr/ma-page/") is None
    assert get_preview_url_for_check_seo("/") is None


def test_get_preview_url_with_prefix_language_admin():
    """Path with language/admin prefix is normalized to preview."""
    url = "/en/admin/cms/placeholder/object/42/edit/100/"
    assert (
        get_preview_url_for_check_seo(url)
        == "/en/admin/cms/placeholder/object/42/preview/100/"
    )
