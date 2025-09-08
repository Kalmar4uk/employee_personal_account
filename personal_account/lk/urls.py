from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "lk"

urlpatterns = [
    path("shifts/", views.shifts, name="shifts"),
    path("auth/", views.auth_for_token, name="auth_for_token")
]
