from django.db import models

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _


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
