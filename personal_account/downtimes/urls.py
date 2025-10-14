from django.urls import path

from . import views

app_name = "downtimes"

urlpatterns = [
    path("", views.downtimes, name="downtime"),
    path("service/<int:id>/", views.downtimes_detail, name="downtime_detail"),
    path(
        "edit-downtime/<int:id>/",
        views.edit_downtimes,
        name="edit_downtime"
    ),
    path("added-downtime/", views.added_downtime, name="added_downtime"),
    path("history-downtime", views.history_downtimes, name="history_downtime")
]
