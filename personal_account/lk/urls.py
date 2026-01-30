from django.urls import path

from . import views

app_name = "lk"

urlpatterns = [
    path(
        "holidays/<int:id>/",
        views.holidays_employee,
        name="holiday_user"
    ),
    path(
        "holidays/group/<int:id>/",
        views.holidays_employees_in_group,
        name="holiday_group"
    ),
    path(
        "birthday/group/<int:id>/",
        views.birthday_employee_group,
        name="birthday_group"
    ),
    path("download/", views.download, name="download"),
    path("generate/", views.generate_default_workshifts, name="generate")
]
