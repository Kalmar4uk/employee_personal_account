from django.contrib import admin
from lk.models import WorkShifts, Holiday


@admin.register(WorkShifts)
class WorkShiftsAdmin(admin.ModelAdmin):
    raw_id_fields = ("employee",)


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    raw_id_fields = ("employee",)
