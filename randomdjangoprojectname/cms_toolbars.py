from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool


class DjangoSeoToolbar(CMSToolbar):

    def populate(self):

        self.toolbar.add_sideframe_item(
            'Check SEO',         # text
            '/django-check-seo?page=' + str(self.request.path),  # url
        )


# register the toolbar
toolbar_pool.register(DjangoSeoToolbar)
