# see https://github.com/kapt-labs/django-check-seo/wiki/Toolbar-shortcut#cms_toolbarspy

# Third party
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _


class DjangoSeoToolbar(CMSToolbar):
    def populate(self):
        # display only if user has permission to access the django-check-seo app
        if self.request.user.has_perm("django_check_seo.use_django_check_seo"):
            self.toolbar.add_sideframe_item(
                _("Check SEO"),
                "/django-check-seo/?page=" + self.request.path,
            )


# register the toolbar
toolbar_pool.register(DjangoSeoToolbar)
