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


# define auth data (for .htaccess files)
DJANGO_CHECK_SEO_AUTH = {}
# update auth data with values from projectname/settings.py
DJANGO_CHECK_SEO_AUTH.update(getattr(settings, "DJANGO_CHECK_SEO_AUTH", {}))


# see https://github.com/kapt-labs/django-check-seo/issues/43 for more informations
DJANGO_CHECK_SEO_AUTH_FOLLOW_REDIRECTS = False
# update redirect with authentication strategy with value from projectname/settings.py
DJANGO_CHECK_SEO_AUTH_FOLLOW_REDIRECTS = getattr(
    settings, "DJANGO_CHECK_SEO_AUTH_FOLLOW_REDIRECTS", False
)

# define http(s) settings (default = use https)
DJANGO_CHECK_SEO_FORCE_HTTP = False
# update http(s) settings with value from projectname/settings.py
DJANGO_CHECK_SEO_FORCE_HTTP = getattr(settings, "DJANGO_CHECK_SEO_FORCE_HTTP", False)


# define css selector to search content into (used for retrieving main content of the page)
DJANGO_CHECK_SEO_SEARCH_IN = {
    "type": "exclude",
    "selectors": ["header", ".cover-section", "#footer"],
}

#
DJANGO_CHECK_SEO_EXCLUDE_CONTENT = getattr(
    settings, "DJANGO_CHECK_SEO_EXCLUDE_CONTENT", ""
)
