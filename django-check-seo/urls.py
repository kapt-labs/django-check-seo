# Third party
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

# Local application / specific library imports
from . import views


urlpatterns = [path("", staff_member_required(views.IndexView.as_view()), name="Index")]
