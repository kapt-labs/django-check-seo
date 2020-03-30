# -*- coding: utf-8 -*-

# Use ./launch_tests.sh to launch these tests.

import re

from bs4 import BeautifulSoup
from django_check_seo.checks import site

html_content = """
<!doctype html>
<html>
    <head>
        <meta name="keywords" content="description,  title">
        <title>Title of the page</title>
    </head>
    <body><p>Content of the page.</p></body>
</html>
"""


class settings:
    def __init__(self):
        self.DJANGO_CHECK_SEO_SETTINGS = {
            "content_words_number": [300, 600],
        }


class init:
    def __init__(self):
        self.keywords = []
        self.problems = []
        self.warnings = []
        self.success = []
        self.settings = settings()
        self.soup = BeautifulSoup(html_content, features="lxml")

        self.content_text = get_content_text(self.soup.find_all("body"))

        self.full_url = "https://localhost/fake-url/title-of-the-page/"
        # populate class with data
        self.page_stats = site.Site(self.soup, self.full_url)


def get_content_text(soup):
    content_text = ""
    for c in soup:
        content_text += c.get_text(separator=" ")

    # strip multiple carriage return (with optional space) to only one
    content_text = re.sub(r"(\n( ?))+", "\n", content_text)
    # strip multiples spaces (>3) to only 2 (for title readability)
    content_text = re.sub(r"   +", "  ", content_text)
    return content_text


def test_url_importance():
    from django_check_seo.checks_list import content_words_number

    assert content_words_number.importance() == 1


def test_content_words_number_short():
    from django_check_seo.checks_list import content_words_number

    site = init()
    content_words_number.run(site)

    for problem in site.problems:
        if problem.name == "Content is too short":
            assert problem.name == "Content is too short"
            assert problem.settings == "at least 300 words, more than 600 if possible"
            assert problem.found == 4
            assert problem.searched_in == ["Content of the page."]
            assert (
                problem.description
                == "Longer articles tend to be better ranked, but will require better writing skills than shorter articles."
            )


def test_content_words_number_short2():
    from django_check_seo.checks_list import content_words_number

    site = init()
    site.soup.find(
        "p"
    ).string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc vel purus mollis eros imperdiet elementum et sit amet orci. Quisque eget posuere ipsum. Vestibulum in tellus in quam congue maximus. Nam cursus, urna a luctus luctus, eros erat accumsan dolor, et porttitor eros quam ut odio. Quisque vel tortor id metus dignissim ullamcorper sit amet ac nunc. Donec laoreet ipsum nulla, sed scelerisque arcu mattis ac. Quisque diam augue, condimentum nec risus nec, rutrum dignissim felis. Nullam interdum tincidunt mauris, eu euismod ligula rutrum vitae. In accumsan, nisi sit amet commodo ornare, risus est dictum nulla, eu egestas quam dui eget felis. In quis imperdiet lectus. Maecenas sit amet quam eu felis maximus venenatis nec non nunc. Nunc nec viverra quam. Quisque sollicitudin ante ex, ut placerat sapien commodo eget. Etiam vel tempor nulla, vitae venenatis risus. Phasellus a euismod ligula. Suspendisse laoreet lacus eget arcu tempor sollicitudin. Sed maximus, diam et interdum commodo, nisi quam varius odio, et dapibus sem ante quis leo. Praesent gravida viverra augue, molestie bibendum mauris sagittis et. Sed sem quam, congue vitae suscipit non, imperdiet at justo. Nullam nunc lacus, dapibus ac felis nec, faucibus ultrices dui. Etiam est sem, ornare vel ipsum non, tincidunt facilisis augue. Vivamus dolor eros, blandit eget feugiat sit amet, mattis in lorem. Pellentesque in luctus mi. Sed varius, felis sed venenatis porta, ipsum dui molestie nulla, in dapibus lacus ligula sed ipsum. Vivamus vitae est est. Vivamus porttitor dui et nisl faucibus pulvinar. Proin ac neque ornare, commodo erat id, maximus sem. Morbi quis nibh rhoncus, sollicitudin turpis sed, ornare erat. Etiam cursus augue a ante dapibus, id dictum nulla sagittis. Fusce volutpat dui sed vehicula ornare. Vivamus et ipsum dapibus, posuere lectus sed, laoreet enim. Duis molestie, nunc at egestas scelerisque, mi dolor vehicula augue, sed pretium lectus odio et lorem. Sed aliquam tortor nec fringilla fermentum. Nulla suscipit nibh ac lacus ornare tempus. Duis at pellentesque urna."

    site.content_text = get_content_text(site.soup.find_all("body"))

    content_words_number.run(site)

    for warning in site.warnings:
        if warning.name == "Content is too short":
            assert warning.name == "Content is too short"
            assert warning.settings == "at least 300 words, more than 600 if possible"
            assert warning.found == 321
            assert warning.searched_in == [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc vel purus mollis eros imperdiet elementum et sit amet orci. Quisque eget posuere ipsum. Vestibulum in tellus in quam congue maximus. Nam cursus, urna a luctus luctus, eros erat accumsan dolor, et porttitor eros quam ut odio. Quisque vel tortor id metus dignissim ullamcorper sit amet ac nunc. Donec laoreet ipsum nulla, sed scelerisque arcu mattis ac. Quisque diam augue, condimentum nec risus nec, rutrum dignissim felis. Nullam interdum tincidunt mauris, eu euismod ligula rutrum vitae. In accumsan, nisi sit amet commodo ornare, risus est dictum nulla, eu egestas quam dui eget felis. In quis imperdiet lectus. Maecenas sit amet quam eu felis maximus venenatis nec non nunc. Nunc nec viverra quam. Quisque sollicitudin ante ex, ut placerat sapien commodo eget. Etiam vel tempor nulla, vitae venenatis risus. Phasellus a euismod ligula. Suspendisse laoreet lacus eget arcu tempor sollicitudin. Sed maximus, diam et interdum commodo, nisi quam varius odio, et dapibus sem ante quis leo. Praesent gravida viverra augue, molestie bibendum mauris sagittis et. Sed sem quam, congue vitae suscipit non, imperdiet at justo. Nullam nunc lacus, dapibus ac felis nec, faucibus ultrices dui. Etiam est sem, ornare vel ipsum non, tincidunt facilisis augue. Vivamus dolor eros, blandit eget feugiat sit amet, mattis in lorem. Pellentesque in luctus mi. Sed varius, felis sed venenatis porta, ipsum dui molestie nulla, in dapibus lacus ligula sed ipsum. Vivamus vitae est est. Vivamus porttitor dui et nisl faucibus pulvinar. Proin ac neque ornare, commodo erat id, maximus sem. Morbi quis nibh rhoncus, sollicitudin turpis sed, ornare erat. Etiam cursus augue a ante dapibus, id dictum nulla sagittis. Fusce volutpat dui sed vehicula ornare. Vivamus et ipsum dapibus, posuere lectus sed, laoreet enim. Duis molestie, nunc at egestas scelerisque, mi dolor vehicula augue, sed pretium lectus odio et lorem. Sed aliquam tortor nec fringilla fermentum. Nulla suscipit nibh ac lacus ornare tempus. Duis at pellentesque urna."
            ]
            assert (
                warning.description
                == "Longer articles tend to be better ranked, but will require better writing skills than shorter articles."
            )


def test_content_words_number_okay():
    from django_check_seo.checks_list import content_words_number

    site = init()
    site.soup.find(
        "p"
    ).string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin eget mollis risus, at tincidunt ipsum. Sed viverra nulla sapien, non lacinia risus rhoncus ut. Proin vitae ante vestibulum, egestas quam eu, rutrum sem. Mauris in commodo eros. Fusce vitae finibus mi, a auctor nulla. Cras eu arcu a lacus congue consectetur vel vel orci. Morbi tempor risus vestibulum molestie tempor. Donec vitae ultricies dolor, non maximus massa. Pellentesque sit amet tincidunt ipsum, id condimentum nulla. Nulla commodo magna ut finibus efficitur. Ut mattis diam metus, vel tristique mi pulvinar et. Pellentesque fermentum ut mauris sit amet fermentum. Phasellus ac nunc vel dolor maximus mattis. Nunc et mauris sit amet nunc malesuada gravida vel feugiat turpis. Pellentesque interdum mattis mauris quis tempor. Pellentesque vehicula mauris et tempus tincidunt. In hac habitasse platea dictumst. Nulla orci dolor, eleifend et varius quis, fringilla sed ipsum. Aliquam erat volutpat. Donec accumsan nec justo at congue. Fusce a erat a massa pulvinar posuere eu quis enim. Nam maximus nunc sem, eget lacinia magna volutpat sit amet. Nam ipsum velit, imperdiet eu lacus ac, faucibus finibus ante. In hac habitasse platea dictumst. Vestibulum in turpis sit amet nibh placerat maximus. Aenean libero erat, tincidunt interdum gravida in, facilisis sit amet magna. Suspendisse pulvinar tincidunt est, id finibus mi volutpat non. Maecenas at condimentum elit, vitae congue metus. Nulla sit amet ullamcorper orci, eget dapibus urna. Pellentesque vitae nisi nec mauris lobortis pharetra non mollis nisi. Morbi ut pretium quam. Nunc dapibus dui dui, nec dignissim mauris aliquam vitae. Nam interdum dolor lacus, vel viverra ligula sollicitudin sit amet. Etiam nec leo eu diam vestibulum varius a vel tellus. Pellentesque nec viverra metus, eu fringilla odio. Valar morghulis luctus varius leo, a congue tortor facilisis ac. Nullam consequat enim ac nulla convallis imperdiet. Sed porttitor auctor pellentesque. Ut pellentesque lectus vel ultricies consequat. Cras nec enim eros. Etiam fringilla quis ante vel dapibus. Morbi tempor arcu magna, id tincidunt ante finibus id. Curabitur ac mauris rhoncus, coucou maman, condimentum lectus. Phasellus ultricies rutrum nisi. Aliquam lacinia ex id malesuada interdum. Curabitur lorem justo, iaculis vel sagittis eget, ornare in erat. Maecenas suscipit dictum volutpat. Pellentesque metus lectus, laoreet ut lacus id, dignissim molestie dui. Ut enim tortor, iaculis vitae pulvinar id, sagittis nec nibh. Curabitur sit amet faucibus velit. Curabitur sed suscipit nunc. Praesent nisi ligula, tempor id aliquam sit amet, fringilla aliquam metus. Nam bibendum blandit turpis quis feugiat. Aenean iaculis ipsum ac felis rutrum, et mollis lacus interdum. Mauris auctor nunc vitae mi pulvinar consectetur. Praesent porttitor diam nec ex placerat ornare. Etiam eu dapibus lacus. Morbi nec nibh varius, lacinia nulla vel, placerat leo. AD il a des lunettes. Duis nisi ligula, finibus non leo dapibus, euismod accumsan neque. Pellentesque tincidunt fringilla dolor eu eleifend. Nam vestibulum nulla vel risus ultrices posuere ut ornare est. Aliquam erat volutpat. Duis arcu enim, posuere in nunc eu, consequat porttitor nisl. Morbi interdum tincidunt erat, ac efficitur risus. Suspendisse potenti. Nulla at convallis massa. Aenean eros dui, facilisis mattis diam a, dignissim ultricies nunc. Vestibulum quis elit id mauris elementum auctor. Sed nec nunc molestie, lacinia erat id, elementum nisi. Maecenas eget porttitor urna. Nunc facilisis iaculis diam a imperdiet. Aenean imperdiet aliquam varius. Nullam nec tempor urna. Donec sapien urna, fermentum et faucibus vehicula, dignissim in dui. Vivamus scelerisque, risus at dictum hendrerit, magna arcu pellentesque orci, et faucibus augue urna sit amet erat. Nullam ullamcorper massa orci, nec feugiat enim scelerisque et. Morbi mollis dui at orci dictum tincidunt. Vivamus ut suscipit mauris. Donec iaculis, nibh id consectetur elementum, ligula nibh maximus tellus, ac efficitur est augue eu ligula. Pellentesque id."

    site.content_text = get_content_text(site.soup.find_all("body"))

    content_words_number.run(site)

    for success in site.success:
        if success.name == "Content length is right":
            assert success.name == "Content length is right"
            assert success.settings == "at least 300 words, more than 600 if possible"
            assert success.found == 606
            assert success.searched_in == [
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin eget mollis risus, at tincidunt ipsum. Sed viverra nulla sapien, non lacinia risus rhoncus ut. Proin vitae ante vestibulum, egestas quam eu, rutrum sem. Mauris in commodo eros. Fusce vitae finibus mi, a auctor nulla. Cras eu arcu a lacus congue consectetur vel vel orci. Morbi tempor risus vestibulum molestie tempor. Donec vitae ultricies dolor, non maximus massa. Pellentesque sit amet tincidunt ipsum, id condimentum nulla. Nulla commodo magna ut finibus efficitur. Ut mattis diam metus, vel tristique mi pulvinar et. Pellentesque fermentum ut mauris sit amet fermentum. Phasellus ac nunc vel dolor maximus mattis. Nunc et mauris sit amet nunc malesuada gravida vel feugiat turpis. Pellentesque interdum mattis mauris quis tempor. Pellentesque vehicula mauris et tempus tincidunt. In hac habitasse platea dictumst. Nulla orci dolor, eleifend et varius quis, fringilla sed ipsum. Aliquam erat volutpat. Donec accumsan nec justo at congue. Fusce a erat a massa pulvinar posuere eu quis enim. Nam maximus nunc sem, eget lacinia magna volutpat sit amet. Nam ipsum velit, imperdiet eu lacus ac, faucibus finibus ante. In hac habitasse platea dictumst. Vestibulum in turpis sit amet nibh placerat maximus. Aenean libero erat, tincidunt interdum gravida in, facilisis sit amet magna. Suspendisse pulvinar tincidunt est, id finibus mi volutpat non. Maecenas at condimentum elit, vitae congue metus. Nulla sit amet ullamcorper orci, eget dapibus urna. Pellentesque vitae nisi nec mauris lobortis pharetra non mollis nisi. Morbi ut pretium quam. Nunc dapibus dui dui, nec dignissim mauris aliquam vitae. Nam interdum dolor lacus, vel viverra ligula sollicitudin sit amet. Etiam nec leo eu diam vestibulum varius a vel tellus. Pellentesque nec viverra metus, eu fringilla odio. Valar morghulis luctus varius leo, a congue tortor facilisis ac. Nullam consequat enim ac nulla convallis imperdiet. Sed porttitor auctor pellentesque. Ut pellentesque lectus vel ultricies consequat. Cras nec enim eros. Etiam fringilla quis ante vel dapibus. Morbi tempor arcu magna, id tincidunt ante finibus id. Curabitur ac mauris rhoncus, coucou maman, condimentum lectus. Phasellus ultricies rutrum nisi. Aliquam lacinia ex id malesuada interdum. Curabitur lorem justo, iaculis vel sagittis eget, ornare in erat. Maecenas suscipit dictum volutpat. Pellentesque metus lectus, laoreet ut lacus id, dignissim molestie dui. Ut enim tortor, iaculis vitae pulvinar id, sagittis nec nibh. Curabitur sit amet faucibus velit. Curabitur sed suscipit nunc. Praesent nisi ligula, tempor id aliquam sit amet, fringilla aliquam metus. Nam bibendum blandit turpis quis feugiat. Aenean iaculis ipsum ac felis rutrum, et mollis lacus interdum. Mauris auctor nunc vitae mi pulvinar consectetur. Praesent porttitor diam nec ex placerat ornare. Etiam eu dapibus lacus. Morbi nec nibh varius, lacinia nulla vel, placerat leo. AD il a des lunettes. Duis nisi ligula, finibus non leo dapibus, euismod accumsan neque. Pellentesque tincidunt fringilla dolor eu eleifend. Nam vestibulum nulla vel risus ultrices posuere ut ornare est. Aliquam erat volutpat. Duis arcu enim, posuere in nunc eu, consequat porttitor nisl. Morbi interdum tincidunt erat, ac efficitur risus. Suspendisse potenti. Nulla at convallis massa. Aenean eros dui, facilisis mattis diam a, dignissim ultricies nunc. Vestibulum quis elit id mauris elementum auctor. Sed nec nunc molestie, lacinia erat id, elementum nisi. Maecenas eget porttitor urna. Nunc facilisis iaculis diam a imperdiet. Aenean imperdiet aliquam varius. Nullam nec tempor urna. Donec sapien urna, fermentum et faucibus vehicula, dignissim in dui. Vivamus scelerisque, risus at dictum hendrerit, magna arcu pellentesque orci, et faucibus augue urna sit amet erat. Nullam ullamcorper massa orci, nec feugiat enim scelerisque et. Morbi mollis dui at orci dictum tincidunt. Vivamus ut suscipit mauris. Donec iaculis, nibh id consectetur elementum, ligula nibh maximus tellus, ac efficitur<span class="good">est augue eu ligula. Pellentesque id.</span>'
            ]
            assert (
                success.description
                == "Longer articles tend to be better ranked, but will require better writing skills than shorter articles."
            )
