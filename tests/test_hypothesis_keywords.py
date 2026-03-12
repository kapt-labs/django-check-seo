# Property-based (fuzzy) tests for keyword-related logic.

import pytest

try:
    from hypothesis import given
    from hypothesis import strategies as st
except ImportError:
    pytest.skip("hypothesis not installed", allow_module_level=True)

# Keywords and text are used in regex patterns; avoid regex-special characters.
_safe_text = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N", "Zs"),
        whitelist_characters="'-",
    ),
    max_size=300,
)
_safe_keyword = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N"),
        whitelist_characters="'-",
    ),
    min_size=1,
    max_size=30,
)


@given(
    text=st.text(alphabet=st.characters(blacklist_categories=("Cs",)), max_size=2000)
)
def test_parse_keywords_text_returns_list_of_non_empty_strings(text):
    """_parse_keywords_text always returns a list of non-empty strings."""
    from django_check_seo.views import _parse_keywords_text

    result = _parse_keywords_text(text)
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, str)
        assert len(item) > 0
        assert item == item.strip()


@given(text=st.one_of(st.none(), st.just(""), st.just("   "), st.just("\n\t")))
def test_parse_keywords_text_empty_or_whitespace_returns_empty_list(text):
    """_parse_keywords_text returns [] for None, empty or whitespace-only string."""
    from django_check_seo.views import _parse_keywords_text

    assert _parse_keywords_text(text) == []


@given(
    keywords=st.lists(
        st.text(
            alphabet=st.characters(blacklist_categories=("Cs",)),
            min_size=1,
            max_size=50,
        ),
        min_size=0,
        max_size=20,
    )
)
def test_parse_keywords_text_roundtrip_via_comma(keywords):
    """Parsing a comma-joined string of keywords yields the same list (modulo order if no dupes)."""
    from django_check_seo.views import _parse_keywords_text

    if not keywords:
        return
    # Avoid commas/newlines in keywords for a simple roundtrip
    safe = [k.replace(",", " ").replace("\n", " ").strip() for k in keywords]
    safe = [k for k in safe if k]
    if not safe:
        return
    text = ", ".join(safe)
    result = _parse_keywords_text(text)
    assert sorted(result) == sorted(safe)


@given(s=st.text(alphabet=st.characters(blacklist_categories=("Cs",)), max_size=500))
def test_normalize_apostrophes_no_crash(s):
    """normalize_apostrophes accepts any string without raising."""
    from django_check_seo.checks.utils import normalize_apostrophes

    out = normalize_apostrophes(s)
    assert isinstance(out, str)
    assert "'" not in out or "\u2019" in out


@given(
    text=_safe_text,
    keywords=st.lists(_safe_keyword, min_size=0, max_size=15),
)
def test_highlight_keywords_in_text_shape(text, keywords):
    """highlight_keywords_in_text returns (str, list of ints, str); occurrence list length = len(keywords)."""
    from django_check_seo.checks.utils import highlight_keywords_in_text

    highlighted, occurrence_list, found_str = highlight_keywords_in_text(
        text.lower(), keywords, normalize_apostrophes_flag=False
    )
    assert isinstance(highlighted, str)
    assert isinstance(occurrence_list, list)
    assert len(occurrence_list) == len(keywords)
    for n in occurrence_list:
        assert isinstance(n, int)
        assert n >= 0
    assert isinstance(found_str, str)


@given(keyword=_safe_keyword, text=_safe_text)
def test_count_keyword_occurrences_non_negative(keyword, text):
    """count_keyword_occurrences returns a non-negative integer."""
    from django_check_seo.checks.utils import count_keyword_occurrences

    n = count_keyword_occurrences(keyword.lower(), text.lower(), for_url=False)
    assert isinstance(n, int)
    assert n >= 0
