from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from lk.models import WorkShifts
from users.models import GroupJob, User


class WorkShiftsTemplate(admin.TabularInline):
    model = WorkShifts
    extra = 0


@admin.register(User)
class MyUserAdmin(UserAdmin):
    inlines = [WorkShiftsTemplate]
    search_fields = ("username", "email", "first_name", "last_name")
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "job_title"
    )
    list_filter = ("is_active",)
    ordering = ("-date_joined",)
    filter_horizontal = ("group_job", "groups")
    fieldsets = (
        (None, {"fields": (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        )}),
        (
            ("Сотрудник"),
            {
                "fields": (
                    "personnel_number",
                    "job_title",
                    "group_job",
                    "is_main"
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups"
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
        (_("Personal info"), {
            "fields": (
                "first_name", "last_name"
            )
        }
        ),
        (
            _("Сотрудник"),
            {
                "fields": (
                    "personnel_number",
                    "job_title",
                    "group_job"
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups"
                ),
            },
        ),
    )


@admin.register(GroupJob)
class GroupJobAdmin(admin.ModelAdmin):
    pass
