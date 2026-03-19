import importlib
import json
import re
from urllib.parse import quote, urlparse

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
from .utils.cms_url_resolution import (
    get_cms_url_for_check_seo,
    get_preview_url_for_check_seo,
)
from .utils.keywords_discovery import get_cms_page_id_language_for_path


def _quote_path(path):
    """Quote path for use in query string (encode slashes so one param is parsed correctly)."""
    return quote(path or "", safe="")


def _parse_keywords_text(text):
    """Parse keywords from text (comma or newline separated), return list of stripped non-empty strings."""
    if not text or not text.strip():
        return []
    parts = re.split(r"[\n,]+", text)
    return [p.strip() for p in parts if p.strip()]


def _normalize_path(path):
    if not path:
        return ""
    path = (path or "").strip()
    if path and not path.startswith("/"):
        path = "/" + path
    return path or "/"


def _get_keywords_for_path(path):
    """Return list of keyword names for the given page path, or []."""
    path = _normalize_path(path)
    if not path or path == "/":
        return []
    try:
        page = Page.objects.get(path=path)
        return [kw.name for kw in page.keywords.all()]
    except Page.DoesNotExist:
        return []


def _get_keywords_for_cms_page(cms_page_id, language):
    """Return list of keyword names for the given (cms_page_id, language), or []."""
    if cms_page_id is None:
        return []
    page = Page.objects.filter(cms_page_id=cms_page_id, language=language or "").first()
    if not page:
        return []
    return [kw.name for kw in page.keywords.all()]


def _get_keywords_for_page_identifier(path=None, cms_page_id=None, language=None):
    """Return keyword names for the page identified by path or (cms_page_id, language)."""
    if cms_page_id is not None:
        return _get_keywords_for_cms_page(cms_page_id, language)
    return _get_keywords_for_path(path or "")


def _get_or_create_page_for_edit(path=None, cms_page_id=None, language=None):
    """
    Get or create Page by path or (cms_page_id, language). Return (page, path_display, use_cms_id).
    """
    if cms_page_id is not None:
        page, _ = Page.objects.get_or_create(
            cms_page_id=cms_page_id,
            language=language or "",
            defaults={"path": None},
        )
        path_display = page.path or f"/cms-page-{cms_page_id}/"
        return (page, path_display, True)
    path = _normalize_path(path)
    if not path:
        path = "/"
    page, _ = Page.objects.get_or_create(path=path, defaults={})
    return (page, path, False)


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

        page = self.request.GET.get("page")
        preview_url = get_preview_url_for_check_seo(page)
        if preview_url:
            url_to_fetch = preview_url
            client = Client()
            client.force_login(self.request.user)
            response = client.get(url_to_fetch, follow=True)
            analysis_draft = True
        else:
            url_to_fetch = get_cms_url_for_check_seo(page)
            if url_to_fetch is None:
                url_to_fetch = page
            client = Client()
            response = client.get(url_to_fetch, follow=True)
            analysis_draft = False

        soup = BeautifulSoup(response.content, features="lxml")

        # populate class with data (use url_to_fetch so full_url is the page we actually checked)
        page_stats = site.Site(soup, url_to_fetch)

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

        context["analysis_draft"] = analysis_draft
        context["settings"] = json.dumps(settings.DJANGO_CHECK_SEO_SETTINGS, indent=4)
        context["html"] = page_stats.content
        context["text"] = page_stats.content_text
        context["keywords"] = page_stats.keywords
        discovery_method = settings.DJANGO_CHECK_SEO_KEYWORDS_DISCOVERY_METHOD
        context["keywords_editable"] = settings.DJANGO_CHECK_SEO_KEYWORDS_EDITABLE and (
            "model_keywords" in discovery_method
            or "django_cms_model_keywords" in discovery_method
        )
        # For form: identify page by path and/or (cms_page_id, language) when using django_cms_model_keywords
        path_for_display = url_to_fetch
        path_for_resolution = (
            urlparse(url_to_fetch or "/").path if url_to_fetch else "/"
        )
        if not path_for_resolution or path_for_resolution == "/":
            path_for_resolution = "/"
        cms_page_id, cms_language = get_cms_page_id_language_for_path(
            path_for_resolution
        )
        use_cms_page_id = (
            context["keywords_editable"]
            and "django_cms_model_keywords" in discovery_method
            and cms_page_id is not None
        )
        context["current_page_path"] = path_for_display
        context["use_cms_page_id"] = use_cms_page_id
        context["current_page_cms_id"] = cms_page_id if use_cms_page_id else None
        context["current_page_language"] = cms_language if use_cms_page_id else None
        if context["keywords_editable"]:
            base = self.request.path.rstrip("/")
            context["keywords_edit_url"] = base + "/keywords-edit/"
            if use_cms_page_id:
                context["keywords_cancel_url"] = (
                    base
                    + "/keywords-edit/?cms_page_id="
                    + str(cms_page_id)
                    + "&language="
                    + quote(cms_language or "", safe="")
                    + "&show_form=0"
                )
                context["checks_refresh_url"] = (
                    self.request.path
                    + "?page="
                    + _quote_path(path_for_display)
                    + "&fragment=checks"
                )
            else:
                context["keywords_cancel_url"] = (
                    base
                    + "/keywords-edit/?path="
                    + _quote_path(path_for_display)
                    + "&show_form=0"
                )
                context["checks_refresh_url"] = (
                    self.request.path
                    + "?page="
                    + _quote_path(path_for_display)
                    + "&fragment=checks"
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


def _base_urls(request, path_value=None, cms_page_id=None, language=None):
    """Build keywords_edit_url and keywords_cancel_url for the fragment."""
    base = request.path
    if cms_page_id is not None:
        cancel = (
            base
            + "?cms_page_id="
            + str(cms_page_id)
            + "&language="
            + quote(language or "", safe="")
            + "&show_form=0"
        )
    else:
        cancel = base + "?path=" + _quote_path(path_value or "") + "&show_form=0"
    return {
        "keywords_edit_url": base,
        "keywords_cancel_url": cancel,
    }


class KeywordsEditView(PermissionRequiredMixin, generic.View):
    """GET: return keywords form fragment (form or list). POST: save keywords and return list fragment + HX-Trigger."""

    permission_required = "django_check_seo.use_django_check_seo"

    def get(self, request):
        path_value = request.GET.get("path") or ""
        cms_page_id = request.GET.get("cms_page_id")
        if cms_page_id is not None:
            try:
                cms_page_id = int(cms_page_id)
            except (TypeError, ValueError):
                cms_page_id = None
        language = request.GET.get("language") or ""
        keywords = _get_keywords_for_page_identifier(
            path=path_value or None,
            cms_page_id=cms_page_id,
            language=language,
        )
        use_cms = cms_page_id is not None
        context = {
            "keywords": keywords,
            "current_page_path": path_value
            or (f"/cms-page-{cms_page_id}/" if use_cms else ""),
            "message_success": False,
            "keywords_text": ", ".join(keywords),
            "all_keywords": _get_all_keyword_names(),
            "use_cms_page_id": use_cms,
            "current_page_cms_id": cms_page_id if use_cms else None,
            "current_page_language": language if use_cms else None,
            **_base_urls(
                request,
                path_value=path_value,
                cms_page_id=cms_page_id,
                language=language,
            ),
        }
        return render(request, "django_check_seo/keywords_form.html", context)

    def post(self, request):
        path_value = (request.POST.get("path") or "").strip()
        cms_page_id = request.POST.get("cms_page_id")
        if cms_page_id is not None:
            try:
                cms_page_id = int(cms_page_id)
            except (TypeError, ValueError):
                cms_page_id = None
        language = (request.POST.get("language") or "").strip()
        page, path_display, use_cms = _get_or_create_page_for_edit(
            path=path_value if path_value else None,
            cms_page_id=cms_page_id,
            language=language,
        )
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
            "current_page_path": path_display,
            "message_success": True,
            "keywords_text": "",
            "all_keywords": _get_all_keyword_names(),
            "use_cms_page_id": use_cms,
            "current_page_cms_id": page.cms_page_id if use_cms else None,
            "current_page_language": page.language if use_cms else None,
            **_base_urls(
                request,
                path_value=path_display,
                cms_page_id=page.cms_page_id if use_cms else None,
                language=page.language if use_cms else None,
            ),
        }
        response = render(request, "django_check_seo/keywords_form.html", context)
        response["HX-Trigger"] = "refreshChecks"
        return response
