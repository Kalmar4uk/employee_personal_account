from django.urls import path

from . import views

app_name = "lk"

urlpatterns = [
    path("holidays/", views.holidays_employee, name="holiday_user")
]
