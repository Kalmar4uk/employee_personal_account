from calendar import monthrange
from datetime import datetime as dt, timedelta as td, time

from django.utils import timezone
from djangoql.admin import DjangoQLSearchMixin
from utils.constants import CURRENT_YEAR

from lk.models import WorkShifts


class MyDjangoQLSearchMixin(DjangoQLSearchMixin):
    djangoql_completion_enabled_by_default = False


def days_month(month: int | None = None, year: int | None = None) -> list[dt]:
    if not month and not year:
        month = timezone.now().month
        year = timezone.now().year
    elif not year:
        year = timezone.now().year
    elif not month:
        month = timezone.now().month
    _, count_day_month = monthrange(year, month)
    result: list[dt] = []
    for day in range(1, count_day_month + 1):
        result.append(dt(year, month, day))
    return result


def get_holidays_first_and_last_date(
        employee
) -> dict[int, dict[str, str]]:
    holidays_all = employee.holidays.filter(
        date__year=CURRENT_YEAR
    ).order_by(
        "date"
    )
    holidays_result = []
    first_day, last_day = None, None
    for holiday in holidays_all:
        if not holidays_all.filter(date=(holiday.date - td(days=1))).exists():
            first_day = holiday.date
        if not holidays_all.filter(date=(holiday.date + td(days=1))).exists():
            last_day = holiday.date
        if first_day and last_day:
            count = (last_day - first_day) + td(days=1)
            holidays_result.append(
                {
                    "first_day": first_day,
                    "last_day": last_day,
                    "count": count.days
                }
            )
            first_day, last_day = None, None
    return holidays_result


def get_workshift_for_downtime(start_downtime: dt) -> WorkShifts:
    date_start = start_downtime.date()
    time_start = start_downtime.time()
    if time_start < time(9, 0, 0):
        shifts = WorkShifts.objects.get(
            employee__group_job=1,
            date_start=date_start-td(days=1),
            night_shift=True
        )
    elif time_start > time(21, 0, 0):
        shifts = WorkShifts.objects.get(
            employee__group_job=1,
            date_start=date_start,
            night_shift=True
        )
    else:
        shifts = WorkShifts.objects.get(
            employee__group_job=1,
            date_start=date_start,
            type="Сменный",
            night_shift=False
        )
    return shifts


def check_less_current_time(data: dt) -> bool:
    return data < timezone.now()
