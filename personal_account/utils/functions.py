from calendar import monthrange
from datetime import datetime as dt

from django.utils import timezone
from utils.constants import CURRENT_MONTH
from djangoql.admin import DjangoQLSearchMixin


class MyDjangoQLSearchMixin(DjangoQLSearchMixin):
    djangoql_completion_enabled_by_default = False


def days_current_month() -> list[dt]:
    current_month = timezone.now().month
    current_year = timezone.now().year
    _, count_day_month = monthrange(current_year, current_month)
    result = []
    for day in range(1, count_day_month + 1):
        result.append(dt(current_year, current_month, day))
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
