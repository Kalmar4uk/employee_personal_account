from calendar import monthrange
from datetime import date
from datetime import datetime as dt
from datetime import time
from datetime import timedelta as td

from django.shortcuts import get_object_or_404
from django.utils import timezone
from djangoql.admin import DjangoQLSearchMixin

from lk.models import WorkShifts
from users.models import User
from utils.constants import CURRENT_MONTH, CURRENT_YEAR, TIME_FORMAT


class MyDjangoQLSearchMixin(DjangoQLSearchMixin):
    djangoql_completion_enabled_by_default = False


class GetCurrentDate:

    @classmethod
    def current_month(cls) -> int:
        return timezone.now().month

    @classmethod
    def current_year(cls) -> int:
        return timezone.now().year

    @classmethod
    def current_date(cls) -> date:
        return timezone.now().date()


def days_month(month: int | None = None, year: int | None = None) -> list[dt]:
    if not month and not year:
        month = CURRENT_MONTH
        year = CURRENT_YEAR
    elif not year:
        year = CURRENT_YEAR
    elif not month:
        month = CURRENT_MONTH
    _, count_day_month = monthrange(year, month)
    result: list[dt] = []
    for day in range(1, count_day_month + 1):
        result.append(dt(year, month, day))
    return result


def get_holidays_first_and_last_date(
        employee, all=None
) -> list[dict[str, str]]:
    if not all:
        holidays_all = employee.holidays.filter(
            date__year=CURRENT_YEAR
        ).order_by(
            "-date"
        )
    else:
        holidays_all = employee.holidays.all().order_by("-date")
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
                    "year": holiday.date.year,
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
    try:
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
    except WorkShifts.DoesNotExist:
        raise ValueError(
            "Отсутствует смена во время проведения плановых работ. "
            "Необходимо проверить смены и пересоздать плановые работы."
        )
    return shifts


def check_less_current_time(data: dt) -> bool:
    return data < timezone.now()


def check_time_downtime_and_first_reminder(
        start_dowmtime: dt,
        end_downtime: dt,
        first_reminder: dt
) -> bool:
    if (
        start_dowmtime > first_reminder < end_downtime
    ) and (
        first_reminder > timezone.now()
    ):
        return True
    return False


def create_default_workshifts_employee(employee_username: str):
    employee = get_object_or_404(User, username=employee_username)
    days = days_month()

    result_for_save = []

    for day in days:
        if day.weekday() not in [5, 6]:
            result_for_save.append(
                WorkShifts(
                    employee=employee,
                    date_start=day,
                    date_end=day,
                    time_start=dt.strptime("09:00", TIME_FORMAT).time(),
                    time_end=dt.strptime("18:00", TIME_FORMAT).time(),
                )
            )

    WorkShifts.objects.bulk_create(result_for_save)
