from django.views import generic
import requests
import os


class IndexView(generic.base.TemplateView):
    template_name = "default.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        full_url = os.environ['DOMAIN_NAME'] + self.request.GET.get("page", None)
        r = requests.get('http://' + full_url)
        context['parsehtml'] = r.text

        return context
