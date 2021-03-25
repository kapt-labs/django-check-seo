import json

import requests
from bs4 import BeautifulSoup
from django.contrib.sites.models import Site
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

        if settings.DJANGO_CHECK_SEO_FORCE_HTTP:
            protocol = "http://"
        else:
            protocol = "https://"

        # get content of the page
        if "http" not in self.request.GET.get(
            "page", None
        ):  # url like "/fr/article-du-site/"
            full_url = (
                protocol
                + Site.objects.get_current().domain
                + self.request.GET.get("page", None)
            )
        else:  # url like "http://mydomain.ext/en/my-page-name/"
            full_url = self.request.GET.get("page", None)

        # use credentials if provided (pass through .htaccess auth)
        if (
            settings.DJANGO_CHECK_SEO_AUTH
            and settings.DJANGO_CHECK_SEO_AUTH["user"] is not None
            and settings.DJANGO_CHECK_SEO_AUTH["pass"] is not None
        ):
            r = requests.get(
                full_url,
                auth=(
                    settings.DJANGO_CHECK_SEO_AUTH["user"],
                    settings.DJANGO_CHECK_SEO_AUTH["pass"],
                ),
                headers={"Cache-Control": "no-store"},
                allow_redirects=False,
            )
            if (
                300 < r.status_code < 400
                and settings.DJANGO_CHECK_SEO_AUTH_FOLLOW_REDIRECTS
            ):
                r = requests.get(
                    r.headers["Location"],
                    auth=(
                        settings.DJANGO_CHECK_SEO_AUTH["user"],
                        settings.DJANGO_CHECK_SEO_AUTH["pass"],
                    ),
                )
        else:
            r = requests.get(full_url, headers={"Cache-Control": "no-store"})

        soup = BeautifulSoup(r.text, features="lxml")

        # populate class with data
        page_stats = site.Site(soup, full_url)

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
