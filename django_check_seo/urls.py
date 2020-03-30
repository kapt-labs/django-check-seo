# Third party
# hacky trick to add python2 compatibility to a python3 project after python2 eol
import django
from django.contrib.admin.views.decorators import staff_member_required

# Local application / specific library imports
from . import views

version = django.get_version()

if version.startswith("2"):
    from django.urls import path

    urlpatterns = [
        path("", staff_member_required(views.IndexView.as_view()), name="Index")
    ]

else:
    from django.conf.urls import url

    urlpatterns = [
        url("^.*$", staff_member_required(views.IndexView.as_view()), name="Index"),
    ]
