from django.db import models
from django.db.models import Q

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _


class Keyword(models.Model):
    """Keyword used for SEO checks. Unique by name."""

    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("keyword")
        verbose_name_plural = _("keywords")

    def __str__(self):
        return self.name

    def pages_using(self):
        return ", ".join(page.get_display_identifier() for page in self.pages.all())

    pages_using.short_description = _("Pages using this keyword")


class Page(models.Model):
    """
    Page identified by path (e.g. /fr/ma-page/) and/or by (cms_page_id, language).
    M2M to Keyword. Hybrid: use path for apphooks/non-CMS URLs,
    (cms_page_id, language) for CMS pages.
    """

    path = models.CharField(
        _("path"), max_length=500, null=True, blank=True, db_index=True
    )
    cms_page_id = models.PositiveIntegerField(
        _("CMS page id"), null=True, blank=True, db_index=True
    )
    language = models.CharField(_("language"), max_length=10, null=True, blank=True)
    keywords = models.ManyToManyField(
        Keyword,
        related_name="pages",
        blank=True,
        verbose_name=_("keywords"),
    )

    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("pages")
        constraints = [
            models.UniqueConstraint(
                fields=["path"],
                condition=Q(path__isnull=False) & ~Q(path=""),
                name="dcs_unique_page_path_when_set",
            ),
            models.UniqueConstraint(
                fields=["cms_page_id", "language"],
                condition=Q(cms_page_id__isnull=False),
                name="dcs_unique_cms_page_language",
            ),
        ]

    def __str__(self):
        return self.get_display_identifier()

    def get_display_identifier(self):
        """Return path if set, else 'cms_page_id=X (lang)' for display."""
        if self.path:
            return self.path
        if self.cms_page_id is not None:
            lang = self.language or ""
            return f"cms_page_id={self.cms_page_id} ({lang})"
        return ""

    def nb_keywords(self):
        return self.keywords.count()

    nb_keywords.short_description = _("Number of keywords")


class DjangoCheckSEOPermissions(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            (
                "use_django_check_seo",
                _(
                    "View the Check SEO button (if using Django CMS) and use Django Check SEO"
                ),
            ),
        )
