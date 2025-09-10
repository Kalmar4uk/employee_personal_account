import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from users.models import GroupJob, User
from utils.functions import (days_current_month,
                             get_holidays_first_and_last_date)


class CustomLoginView(LoginView):
    def get_success_url(self):
        username = self.request.user.username
        return reverse("users:profile", kwargs={"username": username})


@login_required
def main(request):
    username = request.user.username
    return redirect(reverse("users:profile", kwargs={"username": username}))


@login_required
def profile(request, username):
    employee = User.objects.get(username=username)
    group = employee.group_job.get()

    dates = days_current_month()
    calendar = {}
    for date in dates:
        work = employee.workshifts.filter(date_start=date).first()
        holiday = employee.holidays.filter(date=date).first()
        date_format = date.strftime("%Y-%m-%d")
        if work:
            calendar[date_format] = {
                "type": "day-shift-day",
                "time": f"{work.time_start} - {work.time_end}"
            }
        elif holiday:
            calendar[date_format] = {"type": "day-vacation", "time": "Отпуск"}
        else:
            calendar[date_format] = {"type": "day-off", "time": "Выходной"}

    first_date, last_date = get_holidays_first_and_last_date(employee=employee)

    if first_date and last_date:
        count_days = (last_date - first_date) + timedelta(days=1)

        context = {
            "employee": employee,
            "group": group,
            "first_date": first_date,
            "last_date": last_date,
            "count_days": count_days.days,
            "calendar": json.dumps(calendar, cls=DjangoJSONEncoder)
        }
    else:

        context = {
            "employee": employee,
            "group": group,
            "calendar": json.dumps(calendar, cls=DjangoJSONEncoder)
        }

    return render(request, "profile.html", context)


@login_required
def groups(request):
    groups = GroupJob.objects.all().prefetch_related("users")
    context = {
        "groups": groups
    }
    return render(request, "groups.html", context)


@login_required
def groups_detail(request, id):
    group = GroupJob.objects.get(id=id)
    employees = group.users.all()
    work_employees = []
    count_work = 0
    boss = ""
    for employee in employees:
        if employee.is_main:
            boss = employee
        holiday = employee.holidays.filter(
            date=timezone.now(),
        ).exists()
        work = employee.workshifts.filter(date_start=timezone.now())
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
                    "work": work
                }
            )
            count_work += 1
    context = {
        "group": group,
        "work_employees": work_employees,
        "count_work": count_work,
        "boss": boss
    }
    return render(request, "groups_detail.html", context)
