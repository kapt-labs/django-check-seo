# Third party
from django.urls import path

# Local application / specific library imports
from . import views


urlpatterns = [path("", views.IndexView.as_view(), name="Index")]
