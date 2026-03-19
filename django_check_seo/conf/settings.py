# Third party
from django.conf import settings

# define basic SEO settings, see
DJANGO_CHECK_SEO_SETTINGS = {
    "content_words_number": [300, 600],
    "internal_links": 1,
    "external_links": 1,
    "meta_title_length": [30, 60],
    "meta_description_length": [50, 160],
    "keywords_in_first_words": 50,
    "max_link_depth": 4,
    "max_url_length": 70,
}
# update settings redefined in projectname/settings.py
DJANGO_CHECK_SEO_SETTINGS.update(getattr(settings, "DJANGO_CHECK_SEO_SETTINGS", {}))

# define css selector to search content into (used for retrieving main content of the page)
DJANGO_CHECK_SEO_SEARCH_IN = {
    "type": "exclude",
    "selectors": ["header", ".cover-section", "#footer"],
}

#
DJANGO_CHECK_SEO_EXCLUDE_CONTENT = getattr(
    settings, "DJANGO_CHECK_SEO_EXCLUDE_CONTENT", ""
)

# Keywords discovery: import path to a function (site) -> None that sets site.keywords.
# Built-in: django_check_seo.utils.keywords_discovery.meta_keywords (from meta tag),
#          django_check_seo.utils.keywords_discovery.model_keywords (from Page/Keyword by path),
#          django_check_seo.utils.keywords_discovery.django_cms_model_keywords (by cms_page_id+language, fallback path).
DJANGO_CHECK_SEO_KEYWORDS_DISCOVERY_METHOD = getattr(
    settings,
    "DJANGO_CHECK_SEO_KEYWORDS_DISCOVERY_METHOD",
    "django_check_seo.utils.keywords_discovery.meta_keywords",
)

# When True and discovery is model_keywords or django_cms_model_keywords, show editable keywords form.
DJANGO_CHECK_SEO_KEYWORDS_EDITABLE = getattr(
    settings, "DJANGO_CHECK_SEO_KEYWORDS_EDITABLE", False
)

# When True, resolve Django CMS edit/preview URLs to the public page URL for SEO checks (default True).
# When the "page" param is a CMS edit or preview URL, it is resolved via PageContent/Page models.
DJANGO_CHECK_SEO_CMS_EDIT_URL_TO_PUBLIC = getattr(
    settings, "DJANGO_CHECK_SEO_CMS_EDIT_URL_TO_PUBLIC", True
)
