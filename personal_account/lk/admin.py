from django.contrib import admin
from lk.models import Holiday, WorkShifts
from utils.functions import MyDjangoQLSearchMixin


@admin.register(WorkShifts)
class WorkShiftsAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    search_fields = ("employee",)
    list_display = (
        "employee",
        "date_start",
        "date_end",
        "time_start",
        "time_end",
        "night_shift"
    )
    list_filter = (
        "employee",
        "date_start",
        "date_end",
        "time_start",
        "time_end",
        "night_shift"
    )
    raw_id_fields = ("employee",)
    readonly_fields = ("updated_at",)


@admin.register(Holiday)
class HolidayAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    search_fields = ("employee",)
    list_display = ("employee", "date", "status", "type")
    list_filter = ("employee", "date", "status")
    raw_id_fields = ("employee",)
    readonly_fields = ("updated_at",)
