# Third party
from django.utils.translation import gettext as _


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    """Count number of words in content.
    """

    nb_words = len(site.content_text.split())

    # too few words
    if nb_words < site.settings.SEO_SETTINGS["content_words_number"][0]:
        site.problems.append(
            {
                "name": _("Content is too short"),
                "settings": "at least {min} words, more than {min2} if possible, found {nb_words}".format(
                    min=site.settings.SEO_SETTINGS["content_words_number"][0],
                    min2=site.settings.SEO_SETTINGS["content_words_number"][1],
                    nb_words=nb_words,
                ),
                "description": _(
                    'Yoast provide us some knowledge : "A blog post should contain at least 300 words in order to rank well in the search engines. Long posts will rank more easily than short posts. However, long posts require strong writing skills" (<a href="https://yoast.com/blog-post-length/">source</a>).<br />An article from Forbes from 2017 says that "<i>content with 1,000 words or more tends to attract significantly more links and shares</i>", and "<i>the average content length for top 3 rankings was about 750 words, while the average content length for position 20 rankings was about 500 words</i>" (<a href="https://web.archive.org/web/20190708230659/http://www.forbes.com/">source</a>).'
                ),
            }
        )

    elif nb_words < site.settings.SEO_SETTINGS["content_words_number"][1]:
        site.warnings.append(
            {
                "name": _("Content is too short"),
                "settings": "at least {min} words, more than {min2} if possible, found {nb_words}".format(
                    min=site.settings.SEO_SETTINGS["content_words_number"][0],
                    min2=site.settings.SEO_SETTINGS["content_words_number"][1],
                    nb_words=nb_words,
                ),
                "description": _(
                    'Yoast provide us some knowledge : "A blog post should contain at least 300 words in order to rank well in the search engines. Long posts will rank more easily than short posts. However, long posts require strong writing skills" (<a href="https://yoast.com/blog-post-length/">source</a>).<br />An article from Forbes from 2017 says that "<i>content with 1,000 words or more tends to attract significantly more links and shares</i>", and "<i>the average content length for top 3 rankings was about 750 words, while the average content length for position 20 rankings was about 500 words</i>" (<a href="https://web.archive.org/web/20190708230659/https://www.forbes.com/sites/jaysondemers/2017/07/18/how-long-should-your-content-be-for-optimal-seo/2">source</a>).'
                ),
            }
        )
