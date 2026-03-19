# Tests for get_cms_page_id_language_for_path (without django-cms)


from django_check_seo.utils.keywords_discovery import get_cms_page_id_language_for_path


def test_get_cms_page_id_language_without_cms_returns_none():
    """When django CMS is not installed, path is not resolved to (id, language)."""
    assert get_cms_page_id_language_for_path("/fr/ma-page/") == (None, None)
    assert get_cms_page_id_language_for_path("/") == (None, None)


def test_get_cms_page_id_language_normalizes_path():
    """Path is normalized with leading slash."""
    assert get_cms_page_id_language_for_path("fr/ma-page/") == (None, None)
