from calendar import monthrange
from datetime import datetime as dt

from django.utils import timezone
from djangoql.admin import DjangoQLSearchMixin

from utils.constants import CURRENT_MONTH


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
    result = []
    for day in range(1, count_day_month + 1):
        result.append(dt(year, month, day))
    return result


def get_holidays_first_and_last_date(employee) -> tuple | None:
    holidays_all = employee.holidays.filter(
        date__month__gte=CURRENT_MONTH
    ).order_by(
        "date"
    )
    if not holidays_all:
        return None, None

    first = holidays_all.first()
    last = holidays_all.last()

    return first.date, last.date
