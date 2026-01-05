from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from users.models import User
from utils.functions import get_holidays_first_and_last_date

from openpyxl import Workbook as wb


@login_required
def holidays_employee(request, username):
    user = get_object_or_404(User, username=username)
    holidays = get_holidays_first_and_last_date(user, all=True)

    return render(
        request, "employees/holidays.html", context={"holidays": holidays}
    )


@login_required
def holidays_employees_in_group(request, id):
    employees = User.objects.filter(group_job=id)
    result = []

    for employee in employees:
        result.append(
            {
                "employee": employee,
                "holidays": get_holidays_first_and_last_date(
                    employee, all=True
                )
            }
        )

    return render(
        request,
        "groups/groups_holidays.html",
        context={"holidays": result}
    )


@login_required
def download(request):
    print(request.POST)
    return render(request, "download_files/download.html")
