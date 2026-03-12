from django.db import models

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


class Page(models.Model):
    """Page identified by path (e.g. /fr/ma-page/). M2M to Keyword."""

    path = models.CharField(_("path"), max_length=500, unique=True)
    keywords = models.ManyToManyField(
        Keyword,
        related_name="pages",
        blank=True,
        verbose_name=_("keywords"),
    )

    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("pages")

    def __str__(self):
        return self.path


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
