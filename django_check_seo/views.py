import json

from bs4 import BeautifulSoup
from django.test import Client
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.views import generic

from .checks import site
from .checks_list import launch_checks
from .conf import settings


class IndexView(generic.base.TemplateView):
    template_name = "default.html"

    def get_context_data(self, *args, **kwargs):
        context = super(generic.base.TemplateView, self).get_context_data(
            *args, **kwargs
        )

        client = Client()
        page = self.request.GET.get("page")
        response = client.get(page, follow=True)

        soup = BeautifulSoup(response.content, features="lxml")

        # populate class with data
        page_stats = site.Site(soup, page)

        # magic happens here!
        launch_checks.launch_checks(page_stats)

        # end of magic, get collected problems/warnings/success and put them inside the context
        (context["problems"], context["warnings"], context["success"]) = (
            page_stats.problems,
            page_stats.warnings,
            page_stats.success,
        )

        context["settings"] = json.dumps(settings.DJANGO_CHECK_SEO_SETTINGS, indent=4)
        context["html"] = page_stats.content
        context["text"] = page_stats.content_text
        context["keywords"] = page_stats.keywords

        nb_problems = len(context["problems"])
        nb_warnings = len(context["warnings"])

        # define some fancy-looking text here because it is wayyy to dirty with all the {% trans %} in template
        if nb_problems == 0 and nb_warnings == 0:
            context["nb_problems_warnings"] = _(
                '<strong class="green-bg">No problem</strong> was found on the page!'
            )
        else:
            if nb_problems == 0:
                context["nb_problems_warnings"] = _(
                    '<strong class="green-bg">No problem</strong> found, and '
                )
            else:
                context["nb_problems_warnings"] = '<strong class="red-bg">'
                context["nb_problems_warnings"] += ngettext(
                    "{nb_problems} problem</strong> found, and ",
                    "{nb_problems} problems</strong> found, and ",
                    nb_problems,
                ).format(nb_problems=nb_problems)

            if nb_warnings == 0:
                context["nb_problems_warnings"] += _(
                    '<strong class="green-bg">no warning</strong> raised'
                )
            else:
                context["nb_problems_warnings"] += '<strong class="yellow-bg">'
                context["nb_problems_warnings"] += ngettext(
                    "{nb_warnings} warning</strong> raised",
                    "{nb_warnings} warnings</strong> raised",
                    nb_warnings,
                ).format(nb_warnings=nb_warnings)

        return context
