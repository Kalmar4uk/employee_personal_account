from django.shortcuts import render
from openpyxl import load_workbook
from django.utils import timezone
from users.models import User
from lk.models import WorkShifts, Holiday
from datetime import datetime, timedelta
import calendar


TIME_FORMAT = "%H:%M"


def parse_work_shifts(request):
    wb = load_workbook(filename="data_files/work_shifts.xlsx")
    period = timezone.now().strftime('%B %Y')
    sheet = wb[period]
    night_shift = False
    for row in range(26, 33):
        for data in sheet:
            shift = data[row].value
            if shift is not None:
                if isinstance(shift, datetime):
                    date = shift.date()
                elif shift != "-":
                    last_name, first_name = shift.split(" ", 1)
                    user = User.objects.get(
                        first_name=first_name,
                        last_name=last_name
                    )
                    time = data[24].value
                    if time == "-" and shift is not None:
                        pass  # Для отпуска, вывести в другую
                    else:
                        time_start, time_end = time.split(" - ", 1)
                        if time_start.startswith("21"):
                            night_shift = True
                        if (
                            time_end.endswith("21:00") or
                            time.endswith("09:00")
                        ):
                            type = "Сменный"
                        else:
                            type = "5/2"
                        time_start = datetime.strptime(
                            time_start,
                            TIME_FORMAT
                        ).time()
                        time_end = datetime.strptime(
                            time_end,
                            TIME_FORMAT
                        ).time()
                        WorkShifts.objects.create(
                            employee=user,
                            date_start=date,
                            date_end=(
                                date+timedelta(days=1)
                            ) if night_shift else date,
                            time_start=time_start,
                            time_end=time_end,
                            night_shift=night_shift,
                            type=type
                        )
                        night_shift = False

    return render(request, "for_parse.html")


def create_date(request):
    user = User.objects.get(username="rbespalov")
    current_month = timezone.now().month
    current_year = timezone.now().year
    _, count_day_month = calendar.monthrange(current_year, current_month)
    for day in range(1, count_day_month + 1):
        date = datetime(current_year, current_month, day)
        WorkShifts.objects.create(employee=user, date_start=date, date_end=date)
    return render(request, "for_parse.html")
