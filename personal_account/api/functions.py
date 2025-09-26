from utils.functions import days_current_month


def get_calendar(user):
    dates = days_current_month()
    calendar = []
    for date in dates:
        work = user.workshifts.filter(date_start=date).first()
        holiday = user.holidays.filter(date=date).first()
        if work:
            calendar.append(
                {
                    "date": date.date(),
                    "type": "shifts",
                    "time": (
                        f"{work.time_start.strftime('%H:%M')} - "
                        f"{work.time_end.strftime('%H:%M')}"
                    )
                }
            )
        elif holiday:
            calendar.append(
                {
                    "date": date.date(),
                    "type": "holiday",
                    "time": "Отпуск"
                }
            )
        else:
            calendar.append(
                {
                    "date": date.date(),
                    "type": "day-off",
                    "time": "Выходной"
                }
            )
    return calendar


def get_group_calendar(group):
    result = []
    for user in group.users.all():
        result.append({"user": user.id, "calendar": get_calendar(user=user)})
    return result
