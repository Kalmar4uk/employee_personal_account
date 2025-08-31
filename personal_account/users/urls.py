from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "users"

urlpatterns = [
    path("", views.main, name="main"),
    path("profile/<slug:username>", views.profile, name="profile"),
    path("groups/<int:id>", views.groups_detail, name="groups_detail"),
    path("groups/", views.groups, name="groups"),
    path("auth/login/", views.CustomLoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout")
]
