# -*- coding: utf-8 -*-
"""
Shared utilities for SEO checks.
"""
from __future__ import unicode_literals

import re

# Word boundaries for keyword matching: allow symbols (e.g. ®) before/after keyword,
# not letters (e.g. avoid "art" in "artisanat").
# See this issue for more details:
# https://github.com/kapt-labs/django-check-seo/issues/65
# (previously https://github.com/kapt-labs/django-check-seo/issues/38)
_KEYWORD_BOUNDARY_LEFT = r"(^| |\n|,|\.|!|\?|[^\w'])"
_KEYWORD_BOUNDARY_RIGHT = r"($| |\n|,|\.|!|\?|[^\w'])"
_KEYWORD_BOUNDARY_LEFT_URL = r"(^| |\n|,|\.|!|\?|/|-|[^\w'])"
_KEYWORD_BOUNDARY_RIGHT_URL = r"($| |\n|,|\.|!|\?|/|-|[^\w'])"


def count_keyword_occurrences(keyword, text, for_url=False):
    """Count occurrences of a keyword in text with word boundaries (optional plural s).

    Boundaries include [^\\w'] so symbols like ® before/after the keyword are accepted,
    while letters (e.g. "artisanat" for keyword "art") are not.

    Arguments:
        keyword: The keyword to search (will be used literally in regex).
        text: The text to search in.
        for_url: If True, use URL boundaries (adds / and - as separators).

    Returns:
        int: Number of matches.
    """
    if for_url:
        left, right = _KEYWORD_BOUNDARY_LEFT_URL, _KEYWORD_BOUNDARY_RIGHT_URL
    else:
        left, right = _KEYWORD_BOUNDARY_LEFT, _KEYWORD_BOUNDARY_RIGHT
    # keyword is used literally (caller normalizes apostrophes etc.)
    pattern = left + keyword + r"s?" + right
    return len(re.findall(pattern, text))
