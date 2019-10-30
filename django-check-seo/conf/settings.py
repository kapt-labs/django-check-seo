# Third party
from django.conf import settings


# define basic SEO settings
SEO_SETTINGS = {
    "content_words_number": [700, 1000],
    "internal_links": [1, 15],
    "external_links": [1, 5],
    "keywords_repeat": [2, 5],
    "meta_title_length": [30, 60],
    "meta_description_length": [50, 160],
    "keywords_in_first_words": 80,
    "important_semanticals_tags": ["img", "em", "strong", "i", "b"],
    "minimum_used_semantical_tags": 3,
    "max_link_depth": 3,
}

# update SEO settings with values from projectname/settings.py
SEO_SETTINGS.update(getattr(settings, "DJANGO_CHECK_SEO_SETTINGS", {}))
