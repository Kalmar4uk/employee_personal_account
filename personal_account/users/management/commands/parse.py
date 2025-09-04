from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from lk.models import Holiday, WorkShifts
from openpyxl import Workbook, load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from users.models import User
from utils.constants import (COLUMN_FOR_GSMA, HOLIDAY_FOR_GSMA, TIME_FORMAT,
                             TIME_SHIFT_FOR_GSMA, TYPE_HOLIDAY, TYPE_SHIFTS)

PATH_TO_FILE = f"{settings.BASE_DIR}/data_files/work_shifts.xlsx"


class Command(BaseCommand):
    help = "Команда парсинга графика/отпуска"

    def add_arguments(self, parser):
        parser.add_argument(
            "type_parse",
            type=str,
            help=("Тип парсинга: shifts - смены | holidays - отпуск | all - все"))

    def handle(self, *args, **kwargs):
        type_parse = kwargs["type_parse"]
        try:
            if type_parse == "shifts":
                if parse_work_shifts():
                    self.success()
            elif type_parse == "holidays":
                if parse_work_shifts():
                    self.success()
            elif type_parse == "all":
                if parse_work_shifts() and parse_holidays():
                    self.success()
            else:
                text = "\nНеизвестная команда!\nИспользуй shifts или holidays"
                self.bad(txt=text)
        except ValueError as e:
            self.bad(txt=str(e))

    def success(self):
        self.stdout.write(
            self.style.SUCCESS('Данные из файла загружены')
        )

    def bad(self, txt):
        self.stdout.write(
            self.style.ERROR(txt)
        )


def parse_work_shifts() -> bool:
    try:
        sheet = open_wb()
    except ValueError as e:
        raise ValueError(f"При обработке файла возникла ошибка: {e}")

    for cell in COLUMN_FOR_GSMA:
        for data in sheet:
            shift = data[cell].value
            if isinstance(shift, datetime):
                date = shift.date()
            elif shift != "-" and shift is not None:
                try:
                    last_name, first_name = shift.split(" ", 1)
                except Exception as e:
                    raise ValueError(
                        f"При обработке файла возникла ошибка: {e}\n"
                        f"Необходимо проверить исходные данные"
                    )

                try:
                    user = User.objects.get(
                        last_name=last_name,
                        first_name=first_name
                    )
                except Exception:
                    raise ValueError(
                        f"Сотрудника с именем {first_name} и "
                        f"фамилией {last_name} нет в базе.\n"
                        f"Вероятно нужно добавить."
                    )

                time = data[TIME_SHIFT_FOR_GSMA].value
                if time == "-" and shift is not None:
                    continue
                else:
                    time_start, time_end = time.split(" - ", 1)
                    prepare_time = preparation_time(
                        time=time,
                        time_start=time_start,
                        time_end=time_end
                    )
                    try:
                        WorkShifts.objects.create(
                            employee=user,
                            date_start=date,
                            date_end=(
                                date+timedelta(days=1)
                            ) if prepare_time.get("night_shift") else date,
                            time_start=prepare_time.get("time_start"),
                            time_end=prepare_time.get("time_end"),
                            night_shift=prepare_time.get("night_shift"),
                            type=prepare_time.get("type")
                        )
                    except Exception as e:
                        raise ValueError(
                            f"При записи смен возникла ошибка {e}"
                            f"\n Входные данные: "
                            f"{prepare_time}"
                        )
    return True


def parse_holidays() -> bool:
    try:
        sheet = open_wb()
    except ValueError as e:
        raise ValueError(f"При обработке файла возникла ошибка: {e}")

    for cell in COLUMN_FOR_GSMA:
        for data in sheet:
            data_cell = data[cell].value
            if isinstance(data_cell, datetime):
                date = data_cell.date()
            elif data[HOLIDAY_FOR_GSMA].value == "Отпуск":
                if data_cell is not None and data_cell != "-":
                    try:
                        last_name, first_name = data_cell.split(" ", 1)
                    except Exception as e:
                        raise ValueError(
                            f"При обработке файла возникла ошибка: {e}\n"
                            f"Необходимо проверить исходные данные"
                        )
                    try:
                        user = User.objects.get(
                            last_name=last_name,
                            first_name=first_name
                        )
                    except Exception:
                        raise ValueError(
                            f"Сотрудника с именем {first_name} и "
                            f"фамилией {last_name} нет в базе.\n"
                            f"Вероятно нужно добавить."
                        )
                    if timezone.now().date() < date:
                        status = "Запланирован"
                    else:
                        status = "Завершен"

                    try:
                        Holiday.objects.create(
                            employee=user,
                            date=date,
                            status=status,
                            type=TYPE_HOLIDAY.get("yearly")
                        )
                    except Exception as e:
                        raise ValueError(
                            f"При записи отпуска возникла ошибка {e}"
                            f"\n Входные данные: {user}, {date}, {status}"
                        )
    return True


def open_wb() -> Workbook:
    period = timezone.now().strftime('%B %Y')

    try:
        wb = load_workbook(filename=PATH_TO_FILE)
    except FileNotFoundError as e:
        raise ValueError(e)
    except InvalidFileException as e:
        return ValueError(e)

    try:
        sheet = wb[period]
    except KeyError as e:
        raise ValueError(e)

    return sheet


def preparation_time(
        time, time_start, time_end
) -> dict[str, str | datetime]:

    night_shift = False
    type = ""

    if time_start.startswith("21:00"):
        night_shift = True

    elif (
        time_end.endswith("21:00") or
        time_start.startswith("21:00")
    ):
        type = TYPE_SHIFTS.get("schedule")

    else:
        type = TYPE_SHIFTS.get("standart")

    time_start = datetime.strptime(
        time_start,
        TIME_FORMAT
    ).time()

    time_end = datetime.strptime(
        time_end,
        TIME_FORMAT
    ).time()

    return {
        "night_shift": night_shift,
        "type": type,
        "time_start": time_start,
        "time_end": time_end,
        "type": type
    }
