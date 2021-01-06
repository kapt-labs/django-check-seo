# see https://github.com/kapt-labs/django-check-seo/wiki/Toolbar-shortcut#cms_toolbarspy

# Third party
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from django.utils.translation import ugettext_lazy as _


class DjangoSeoToolbar(CMSToolbar):
    def populate(self):

        self.toolbar.add_sideframe_item(
            _("Check SEO"),  # text
            "/django-check-seo/?page="
            + self.request.path,  # url (+ current page passed as a GET parameter)
        )


# register the toolbar
toolbar_pool.register(DjangoSeoToolbar)
