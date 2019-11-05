# Standard Library
import re

# Third party
from django.utils.translation import gettext as _


def check_h2(self):
    h2 = self.soup.find_all("h2")
    if not h2:
        self.warnings.append(
            {
                "name": _("No h2 tag"),
                "settings": _("at least 1"),
                "description": _(
                    'H2 tags are useful because they are explored by search engines and can help them understand the subject of your page (<a href="https://robsnell.com/matt-cutts-transcript.html">source</a>). It\'s a "section title", so every time you start talking about a new topic, you can put an h2 tag, which will explain what the content will be about.'
                ),
            }
        )
    else:
        occurence = []
        # check if each keyword
        for keyword in self.keywords:
            # is present at least
            for single_h2 in h2:
                occurence.append(
                    sum(
                        1
                        for _ in re.finditer(
                            r"\b%s\b" % re.escape(keyword.lower()),
                            single_h2.text.lower(),
                        )
                    )
                )
        # if no keyword is found in h2
        if not any(i > 0 for i in occurence):
            self.warnings.append(
                {
                    "name": _("No keyword in h2"),
                    "settings": _("at least 1"),
                    "description": _(
                        'Matt Cutts (creator of Google SafeSearch) <a href="https://robsnell.com/matt-cutts-transcript.html">stated in 2009</a> that "[...] we use things in the title, things in the URL, even things that are really highlighted, like h2 tags and stuff like that. ". Even if there is not really a more recent acknowledgement, h2 titles are important (but maybe not as important as h1 & title tags).'
                    ),
                }
            )
