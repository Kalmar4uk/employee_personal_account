from django.contrib import admin
from users.models import User, GroupJob
from django.contrib.auth.admin import UserAdmin
from lk.models import WorkShifts
from django.utils.translation import gettext_lazy as _


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
    filter_horizontal = ("employees",)
