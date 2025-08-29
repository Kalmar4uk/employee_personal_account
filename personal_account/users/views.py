from django.shortcuts import render
from users.models import User, GroupJob
from lk.models import WorkShifts, Holiday
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q


CURRENT_MONTH = timezone.now().month


class CustomLoginView(LoginView):
    def get_success_url(self):
        username = self.request.user.username
        return reverse('users:profile', kwargs={'username': username})


@login_required
def profile(request, username):
    employee = User.objects.get(username=username)
    work_shifts = employee.workshifts.filter(date_start__month=CURRENT_MONTH)
    holidays = employee.holidays.all()
    group = employee.groupsjob.get()

    context = {
        "employee": employee,
        "group": group,
        "work_shifts": work_shifts,
        "holidays": holidays
    }

    return render(request, "profile.html", context)


@login_required
def groups(request):
    groups = GroupJob.objects.all().prefetch_related("employees")
    context = {
        "groups": groups
    }
    return render(request, "groups.html", context)


@login_required
def groups_detail(request, id):
    group = GroupJob.objects.get(id=id)
    employees = group.employees.all()
    work_employees = []
    count_work = 0
    for employee in employees:
        holiday = employee.holidays.filter(date_start__lte=timezone.now(), date_end__gte=timezone.now()).exists()
        work = employee.workshifts.filter(date_start__day=timezone.now().day)
        if holiday:
            work_employees.append({"employee": employee, "work": None, "cause": "holiday"})
        elif not work:
            work_employees.append({"employee": employee, "work": None, "cause": "day_off"})
        else:
            work_employees.append({"employee": employee, "work": work})
            count_work += 1
    context = {
        "group": group,
        "work_employees": work_employees,
        "count_work": count_work
    }
    return render(request, "groups_detail.html", context)
