from datetime import datetime, date as dt

from users.models import GroupJob, User
from utils.functions import days_month


def get_day(
        user: User,
        month: int,
        year: int,
        day: int
) -> list[dict[str, dt]]:
    date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d").date()
    work = user.workshifts.filter(date_start=date).first()
    holiday = user.holidays.filter(date=date).first()
    if not work and holiday:
        day: list[dict[str, dt]] = [
            {
                "date": date,
                "type": "holiday",
                "time": None
            }
        ]
        return day
    if work:
        day: list[dict[str, dt]] = [
            {
                "date": date,
                "type": "shifts",
                "time": {
                    "time_start": work.time_start,
                    "time_end": work.time_end
                }
            }
        ]
        return day


def get_calendar(user: User, month: int, year: int) -> list[dict[str, dt]]:
    dates = days_month(month=month, year=year)
    calendar: list[dict[str, dt]] = []
    for date in dates:
        work = user.workshifts.filter(date_start=date).first()
        holiday = user.holidays.filter(date=date).first()
        if work:
            calendar.append(
                {
                    "date": date.date(),
                    "type": "shifts",
                    "time": {
                        "time_start": work.time_start,
                        "time_end": work.time_end
                    }
                }
            )
        elif holiday:
            calendar.append(
                {
                    "date": date.date(),
                    "type": "holiday",
                    "time": None
                }
            )
        else:
            calendar.append(
                {
                    "date": date.date(),
                    "type": "day-off",
                    "time": None
                }
            )
    return calendar


def get_group_calendar(
        group: GroupJob, month: int, year: int, day: int | None = None
) -> list[dict[str, dt]]:
    result: list[dict[str, dt]] = []
    if day:
        for user in group.users.all():
            result.append(
                {
                    "user": user.id,
                    "calendar": get_day(
                        user=user,
                        month=month,
                        year=year,
                        day=day
                    )
                }
            )
    else:
        for user in group.users.all():
            result.append(
                {
                    "user": user.id,
                    "calendar": get_calendar(user=user, month=month, year=year)
                }
            )
    return result
