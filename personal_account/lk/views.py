from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from users.models import User
from utils.functions import (create_default_workshifts_employee,
                             get_holidays_first_and_last_date)
from utils.parse import holiday, workshifts


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
    if request.method == "POST":
        file = request.FILES.get("file")
        type_line = request.POST.get("group_type")
        try:
            if request.POST.get("data_type") == "shifts":
                workshifts.parse_work_shifts(file=file, type_line=type_line)
            elif request.POST.get("data_type") == "holidays":
                if type_line == "gsma":
                    holiday.parse_holidays_gsma(file=file)
                else:
                    holiday.parse_holidays(file=file, type_line=type_line)
        except ValueError as e:
            return render(
                request,
                "errors/400.html",
                context={"error": e},
                status=400
            )
        return render(request, "download_files/download.html")
    return render(request, "download_files/download.html")


@login_required
def birthday_employee_group(request, id):
    employees = User.objects.filter(
        group_job=id
    ).order_by(
        "-birthday"
    ).values(
        "first_name", "last_name", "birthday"
    )

    context = {"employees": employees}

    return render(request, "groups/groups_birthday.html", context)


@login_required
def generate_default_workshifts(request):
    users = User.objects.filter(
        is_active=True
    ).order_by("last_name", "first_name")
    context = {"users": users}
    if request.method == "POST":
        username = request.POST.get("username")
        user = get_object_or_404(User, username=username)
        create_default_workshifts_employee(employee=user)

    return render(request, "generate_shifts/generate.html", context)
