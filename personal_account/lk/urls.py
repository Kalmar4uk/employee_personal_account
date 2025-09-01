from django.urls import path

from . import views

app_name = "lk"

urlpatterns = [
    path("", views.parse_work_shifts, name="parse"),
]
