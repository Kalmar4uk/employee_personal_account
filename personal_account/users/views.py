import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator

from users.forms import MySetPassword
from users.models import GroupJob, User, DepartmentJob
from utils.constants import DATE_FORMAT, MONTHS
from utils.functions import (GetCurrentDate, days_month,
                             get_holidays_first_and_last_date)


class CustomLoginView(LoginView):
    def get_success_url(self):
        id = self.request.user.id
        return reverse("users:profile", kwargs={"id": id})


def set_password(request):
    form = MySetPassword(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        new_password = form.cleaned_data.get("password")
        user = get_object_or_404(User, username=username)
        if user.check_password(new_password):
            return redirect(reverse("users:login"))
        user.set_password(new_password)
        user.save()
        return redirect(reverse("users:login"))
    return render(
        request,
        "registration/set_password.html",
        context={"form": form}
    )


@login_required
def main(request):
    id = request.user.id
    return redirect(reverse("users:profile", kwargs={"id": id}))


@login_required
def profile(request, id):
    employee = get_object_or_404(User, id=id, is_active=True)
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
        "id",
        "username",
        "first_name",
        "last_name",
        "job_title",
        "group_job__title"
    )

    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}

    return render(request, "employees/employees.html", context)


@login_required
def groups(request):
    departments = DepartmentJob.objects.all().prefetch_related("group_job")
    context = {
        "departments": departments
    }
    return render(request, "groups/groups.html", context)


@login_required
def groups_detail(request, id):
    group = get_object_or_404(GroupJob, id=id)
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

    count_not_work = employees.count() - count_work

    context = {
        "group": group,
        "work_employees": work_employees,
        "count_work": count_work,
        "count_not_works": count_not_work,
        "boss": boss
    }
    return render(request, "groups/groups_detail.html", context)


@login_required
def group_calendar(request, id):

    try:
        month = int(request.GET.get("month", GetCurrentDate.current_month()))
    except ValueError:
        month = GetCurrentDate.current_month()

    try:
        year = int(request.GET.get("year", GetCurrentDate.current_year()))
    except ValueError:
        year = GetCurrentDate.current_year()

    dates = days_month(month=month, year=year)

    group = GroupJob.objects.filter(id=id).prefetch_related("users")

    result = []

    for employees in group:
        for employee in employees.users.all():
            schedule = {}
            for date in dates:
                work = employee.workshifts.filter(date_start=date).first()
                holiday = employee.holidays.filter(date=date).first()
                date_format = date.strftime("%Y-%m-%d")
                if work:
                    schedule[date_format] = {
                        "time": (
                            f"{work.time_start.strftime('%H:%M')} - "
                            f"{work.time_end.strftime('%H:%M')}"
                        ),
                        "type_shift": work.type
                    }
                elif holiday:
                    schedule[date_format] = {
                        "time": "",
                        "type_shift": "Отпуск"
                    }
            user = {
                "id": employee.id,
                "name": f"{employee.last_name} {employee.first_name}",
                "initials": f"{employee.last_name[0]}{employee.first_name[0]}",
                "schedule": schedule
            }
            result.append(user)

    context = {
        "month_data": MONTHS.get(month),
        "year_data": year,
        "month_for_js": month - 1,
        "schedule": json.dumps({"employees": result}, cls=DjangoJSONEncoder)
    }
    return render(request, "groups/groups_calendar.html", context=context)
