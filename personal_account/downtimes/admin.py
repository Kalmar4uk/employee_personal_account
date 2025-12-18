from django.contrib import admin

from downtimes.models import Downtime, ReminderDowntime
from utils.functions import MyDjangoQLSearchMixin


@admin.register(Downtime)
class DowntimeAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin, ):
    search_fields = ("service",)
    list_display = (
        "service",
        "gsma_employee",
        "start_downtime",
        "end_downtime",
        "description",
        "created_at"
    )
    list_filter = (
        "service",
        "gsma_employee",
        "start_downtime",
        "end_downtime"
    )
    readonly_fields = ("created_at",)
    row_id_field = ("gsma_employee",)


@admin.register(ReminderDowntime)
class ReminderDowntimeAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    search_fields = ("downtime",)
    list_display = ("id", "downtime", "first_reminder", "success_reminder")
    list_filter = ("first_reminder", "success_reminder")
    readonly_fields = ("created_at",)
    row_id_field = ("downtime",)
