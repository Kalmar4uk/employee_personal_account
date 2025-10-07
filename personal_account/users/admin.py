from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from lk.models import WorkShifts
from users.models import GroupJob, User
from utils.constants import CURRENT_MONTH
from utils.functions import MyDjangoQLSearchMixin


class WorkShiftsInline(admin.TabularInline):
    model = WorkShifts
    extra = 0

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(
            date_start__month=CURRENT_MONTH
        ).order_by(
            "date_start"
        )


class UserInline(admin.TabularInline):
    model = User.group_job.through
    readonly_fields = ("user",)
    can_delete = False
    extra = 0
    verbose_name_plural = "Сотрудники группы"


@admin.register(User)
class MyUserAdmin(MyDjangoQLSearchMixin, UserAdmin):
    inlines = [WorkShiftsInline]
    search_fields = ("username", "email", "first_name", "last_name")
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "filter_job_group",
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

    @admin.display(description="Группа")
    def filter_job_group(self, obj):
        return ", ".join([group.title for group in obj.group_job.all()])


@admin.register(GroupJob)
class GroupJobAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    inlines = [UserInline]
    list_display = ["title", "boss"]
    readonly_fields = ["boss"]

    def boss(self, obj):
        return obj.users.get(is_main=True)

    boss.short_description = "Руководитель"
