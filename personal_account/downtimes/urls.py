from django.urls import path

from . import views

app_name = "downtimes"

urlpatterns = [
    path("", views.downtimes, name="downtime"),
    path("<int:id>/", views.downtimes_detail, name="downtime_detail"),
    path(
        "<int:id>/edit/",
        views.edit_downtimes,
        name="edit_downtime"
    ),
    path(
        "<int:id>/reminder/<uuid:reminder_id>/",
        views.edit_reminder_downtimes,
        name="edit_reminder"
    ),
    path("create/", views.create_downtime, name="added_downtime"),
    path("history/", views.history_downtimes, name="history_downtime"),
]
