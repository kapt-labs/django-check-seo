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


def normalize_apostrophes(s):
    """Replace straight apostrophe by typographic one for consistent keyword matching."""
    return s.replace("'", "\u2019")  # U+2019 right single quotation mark


def get_heading_text(tag):
    """Return heading text, or img alt if heading only contains an image with alt."""
    if not tag.text and tag.find("img", {"alt": True}):
        return tag.find("img")["alt"]
    return tag.text


def highlight_keywords_in_text(
    text, keywords, normalize_apostrophes_flag=False, for_url=False
):
    """Count keyword occurrences, highlight them with <b class="good">, return found string.

    Arguments:
        text: The text to search in (assumed already lowercased by caller).
        keywords: Iterable of keyword strings.
        normalize_apostrophes_flag: If True, normalize apostrophes in text and keywords.
        for_url: If True, use URL boundaries for counting.

    Returns:
        tuple: (highlighted_text, occurrence_list, found_string)
        - highlighted_text: text with keywords wrapped in <b class="good">...</b>
        - occurrence_list: one int per keyword (count for that keyword)
        - found_string: comma-separated list of keywords that were found
    """
    if normalize_apostrophes_flag:
        text = normalize_apostrophes(text)
    occurrence_list = []
    found_kw = []
    for keyword in keywords:
        kw = keyword.lower()
        if normalize_apostrophes_flag:
            kw = normalize_apostrophes(kw)
        count = count_keyword_occurrences(kw, text, for_url=for_url)
        occurrence_list.append(count)
        if count > 0:
            text = text.replace(kw, '<b class="good">' + kw + "</b>")
            found_kw.append(kw)
    return (text, occurrence_list, ", ".join(found_kw))


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
