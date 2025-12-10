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


@login_required
def holidays_employee(request):
    user = request.user
    holidays = get_holidays_first_and_last_date(user, all=True)
    return render(
        request, "employees/holidays.html", context={"holidays": holidays}
    )
