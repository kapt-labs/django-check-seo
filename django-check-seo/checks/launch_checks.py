def launch_checks(site):
    """All the checks are performed here. Called in get_context_data().
    All function should add a dict in site.problems or site.warnings

    Arguments:
        site {Site} -- A set of useful vars (including problems & warnings, two lists of dict).
    """
    from .check_description import check_description
    from .check_h1 import check_h1
    from .check_h2 import check_h2
    from .check_images import check_images
    from .check_keywords import check_keywords
    from .check_keyword_url import check_keyword_url
    from .check_links import check_links
    from .check_title import check_title
    from .check_url import check_url
    from .content_words_number import content_words_number
    from .count_words import count_words
    from .keyword_present_first_paragraph import keyword_present_first_paragraph

    # add your file here pls

    check_keywords(site)
    check_description(site)
    check_h1(site)
    check_h2(site)
    check_images(site)
    check_keyword_url(site)
    check_links(site)
    check_title(site)
    check_url(site)
    content_words_number(site)
    count_words(site)
    keyword_present_first_paragraph(site)
    # add your function here pls
