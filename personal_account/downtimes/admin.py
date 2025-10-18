from django.contrib import admin
from downtimes.models import Downtime
from utils.functions import MyDjangoQLSearchMixin


@admin.register(Downtime)
class DowntimeAdmin(admin.ModelAdmin, MyDjangoQLSearchMixin):
    search_fields = ("service",)
    list_display = (
        "service",
        "gsma_employee",
        "start_downtime",
        "end_downtime",
        "description"
    )
    list_filter = (
        "service",
        "gsma_employee",
        "start_downtime",
        "end_downtime"
    )
    readonly_fields = ("created_at",)
    row_id_field = ("gsma_employee",)
