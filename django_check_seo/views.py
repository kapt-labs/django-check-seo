import importlib
import json
import re
from urllib.parse import quote

from bs4 import BeautifulSoup
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.test import Client
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.views import generic

from .checks import site
from .checks_list import launch_checks
from .conf import settings
from .models import Keyword, Page


def _quote_path(path):
    """Quote path for use in query string (encode slashes so one param is parsed correctly)."""
    return quote(path or "", safe="")


def _parse_keywords_text(text):
    """Parse keywords from text (comma or newline separated), return list of stripped non-empty strings."""
    if not text or not text.strip():
        return []
    parts = re.split(r"[\n,]+", text)
    return [p.strip() for p in parts if p.strip()]


def _get_keywords_for_path(path):
    """Return list of keyword names for the given page path, or []."""
    if not path:
        return []
    path = path if path.startswith("/") else "/" + path
    try:
        page = Page.objects.get(path=path)
        return [kw.name for kw in page.keywords.all()]
    except Page.DoesNotExist:
        return []


def _get_all_keyword_names():
    """Return sorted list of all keyword names (for datalist autocomplete)."""
    return list(
        Keyword.objects.values_list("name", flat=True).distinct().order_by("name")
    )


def _get_keywords_discovery_function():
    """Resolve the keywords discovery function from settings (import path)."""
    method = settings.DJANGO_CHECK_SEO_KEYWORDS_DISCOVERY_METHOD
    module_path, func_name = method.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)


class IndexView(PermissionRequiredMixin, generic.base.TemplateView):
    template_name = "django_check_seo/default.html"
    permission_required = "django_check_seo.use_django_check_seo"

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

        # populate keywords using configured discovery method (meta or model)
        discovery_func = _get_keywords_discovery_function()
        discovery_func(page_stats)

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
        # Allow editing keywords on this page only when using model storage
        discovery_method = settings.DJANGO_CHECK_SEO_KEYWORDS_DISCOVERY_METHOD
        context["keywords_editable"] = (
            settings.DJANGO_CHECK_SEO_KEYWORDS_EDITABLE
            and "model_keywords" in discovery_method
        )
        context["current_page_path"] = page
        if context["keywords_editable"]:
            base = self.request.path.rstrip("/")
            context["keywords_edit_url"] = base + "/keywords-edit/"
            context["keywords_cancel_url"] = (
                base + "/keywords-edit/?path=" + _quote_path(page) + "&show_form=0"
            )
            context["checks_refresh_url"] = (
                self.request.path + "?page=" + _quote_path(page) + "&fragment=checks"
            )
            context["all_keywords"] = _get_all_keyword_names()

        nb_problems = len(context["problems"])
        nb_warnings = len(context["warnings"])

        # define some fancy-looking text here because it is wayyy to dirty with all the {% translate%} in template
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

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get("fragment") == "checks":
            return render(
                self.request,
                "django_check_seo/fragment_checks.html",
                context,
            )
        return super().render_to_response(context, **response_kwargs)


def _base_urls(request, path_value):
    """Build keywords_edit_url and keywords_cancel_url for the fragment."""
    base = request.path
    return {
        "keywords_edit_url": base,
        "keywords_cancel_url": base
        + "?path="
        + _quote_path(path_value)
        + "&show_form=0",
    }


class KeywordsEditView(PermissionRequiredMixin, generic.View):
    """GET: return keywords form fragment (form or list). POST: save keywords and return list fragment + HX-Trigger."""

    permission_required = "django_check_seo.use_django_check_seo"

    def get(self, request):
        path_value = request.GET.get("path") or ""
        keywords = _get_keywords_for_path(path_value)
        context = {
            "keywords": keywords,
            "current_page_path": path_value,
            "message_success": False,
            "keywords_text": ", ".join(keywords),
            "all_keywords": _get_all_keyword_names(),
            **_base_urls(request, path_value),
        }
        return render(request, "django_check_seo/keywords_form.html", context)

    def post(self, request):
        path_value = (request.POST.get("path") or "").strip()
        if not path_value:
            path_value = "/"
        if not path_value.startswith("/"):
            path_value = "/" + path_value
        page, _ = Page.objects.get_or_create(path=path_value, defaults={})
        action = (request.POST.get("action") or "").strip()

        if action == "update":
            old_name = (request.POST.get("old_keyword") or "").strip()
            new_name = (request.POST.get("new_keyword") or "").strip()
            if old_name and new_name:
                try:
                    old_kw = Keyword.objects.get(name=old_name)
                    new_kw, _ = Keyword.objects.get_or_create(
                        name=new_name, defaults={}
                    )
                    page.keywords.remove(old_kw)
                    page.keywords.add(new_kw)
                except Keyword.DoesNotExist:
                    pass
        elif action == "remove":
            name = (request.POST.get("keyword") or "").strip()
            if name:
                try:
                    kw = Keyword.objects.get(name=name)
                    page.keywords.remove(kw)
                except Keyword.DoesNotExist:
                    pass
        elif action == "add":
            name = (request.POST.get("keyword") or "").strip()
            if name:
                kw, _ = Keyword.objects.get_or_create(name=name, defaults={})
                page.keywords.add(kw)
        else:
            # bulk save (textarea)
            keywords_text = request.POST.get("keywords_text", "")
            names = _parse_keywords_text(keywords_text)
            keyword_objs = []
            for name in names:
                kw, _ = Keyword.objects.get_or_create(name=name.strip(), defaults={})
                keyword_objs.append(kw)
            page.keywords.set(keyword_objs)

        keywords = [kw.name for kw in page.keywords.all()]
        context = {
            "keywords": keywords,
            "current_page_path": path_value,
            "message_success": True,
            "keywords_text": "",
            "all_keywords": _get_all_keyword_names(),
            **_base_urls(request, path_value),
        }
        response = render(request, "django_check_seo/keywords_form.html", context)
        response["HX-Trigger"] = "refreshChecks"
        return response
