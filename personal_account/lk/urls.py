from django.urls import path

from . import views

app_name = "lk"

urlpatterns = [
    path(
        "holidays/<slug:username>/",
        views.holidays_employee,
        name="holiday_user"
    ),
    path(
        "holidays/group/<int:id>/",
        views.holidays_employees_in_group,
        name="holiday_group")
]
