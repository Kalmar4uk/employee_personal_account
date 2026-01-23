import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from users.models import GroupJob, User
from utils.constants import DATE_FORMAT, MONTHS
from utils.functions import (GetCurrentDate, days_month,
                             get_holidays_first_and_last_date)


class CustomLoginView(LoginView):
    def get_success_url(self):
        username = self.request.user.username
        return reverse("users:profile", kwargs={"username": username})


def set_password(request):
    if request.POST:
        username = request.POST.get("username")
        new_password = request.POST.get("password")
        user = get_object_or_404(User, username=username)
        if user.check_password(new_password):
            pass
        user.set_password(new_password)
        user.save()
        return redirect(reverse("users:login"))
    return render(request, "registration/set_password.html")


@login_required
def main(request):
    username = request.user.username
    return redirect(reverse("users:profile", kwargs={"username": username}))


@login_required
def profile(request, username):
    employee = get_object_or_404(User, username=username)
    group = employee.group_job.filter().first()

    try:
        month = int(request.GET.get("month", GetCurrentDate.current_month()))
    except ValueError:
        month = GetCurrentDate.current_month()

    try:
        year = int(request.GET.get("year", GetCurrentDate.current_year()))
    except ValueError:
        year = GetCurrentDate.current_year()

    dates = days_month(month=month, year=year)

    calendar = {}
    for date in dates:
        work = employee.workshifts.filter(date_start=date).first()
        holiday = employee.holidays.filter(date=date).first()
        date_format = date.strftime("%Y-%m-%d")
        if work:
            calendar[date_format] = {
                "type": (
                    "day-night-shift"
                    if work.night_shift
                    else "day-shift-day"
                ),
                "time": (
                    f"{work.time_start.strftime('%H:%M')} - "
                    f"{work.time_end.strftime('%H:%M')}"
                )
            }
        elif holiday:
            calendar[date_format] = {"type": "day-vacation", "time": ""}
        else:
            calendar[date_format] = {"type": "day-off", "time": ""}

    holidays = get_holidays_first_and_last_date(employee=employee)

    context = {
        "employee": employee,
        "group": group,
        "holidays": holidays,
        "month_data": MONTHS.get(month),
        "year_data": year,
        "month_for_js": month - 1,
        "calendar": json.dumps(calendar, cls=DjangoJSONEncoder)
    }

    return render(request, "employees/profile.html", context)


@login_required
def employees(request):
    employees = User.objects.filter(
        is_active=True
    ).exclude(
        username="admin"
    ).order_by(
        "last_name",
        "first_name"
    ).values(
        "username",
        "first_name",
        "last_name",
        "job_title",
        "group_job__title"
    )

    context = {"employees": employees}

    return render(request, "employees/employees.html", context)


@login_required
def groups(request):
    groups = GroupJob.objects.all().prefetch_related("users")
    context = {
        "groups": groups
    }
    return render(request, "groups/groups.html", context)


@login_required
def groups_detail(request, id):
    group = GroupJob.objects.get(id=id)
    employees = group.users.filter(
        is_active=True
    ).order_by("last_name", "first_name")
    try:
        date = request.GET.get("date", GetCurrentDate.current_date())
        if isinstance(date, str):
            date = datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        date = timezone.now()

    work_employees = []
    count_work = 0
    boss = ""
    for employee in employees:
        if employee.is_main:
            boss = employee
        holiday = employee.holidays.filter(
            date=date,
        ).exists()
        work = employee.workshifts.filter(date_start=date)
        if holiday:
            work_employees.append(
                {
                    "employee": employee,
                    "work": None,
                    "cause": "holiday"
                }
            )
        elif not work:
            work_employees.append(
                {
                    "employee": employee,
                    "work": None,
                    "cause": "day_off"
                }
            )
        else:
            work_employees.append(
                {
                    "employee": employee,
                    "work": work,
                }
            )
            count_work += 1
    context = {
        "group": group,
        "work_employees": work_employees,
        "count_work": count_work,
        "boss": boss
    }
    return render(request, "groups/groups_detail.html", context)
