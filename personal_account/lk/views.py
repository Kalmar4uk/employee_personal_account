from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from utils.functions import get_holidays_first_and_last_date


@login_required
def holidays_employee(request):
    user = request.user
    holidays = get_holidays_first_and_last_date(user, all=True)
    return render(
        request, "employees/holidays.html", context={"holidays": holidays}
    )
