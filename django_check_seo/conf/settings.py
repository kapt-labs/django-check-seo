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
