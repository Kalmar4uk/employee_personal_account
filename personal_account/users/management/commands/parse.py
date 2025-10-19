from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from lk.models import Holiday, WorkShifts
from openpyxl import Workbook, load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from users.models import User
from utils.constants import (CHOICES_STATUS_HOLIDAY, COLUMN_FOR_LINE,
                             HOLIDAY_FOR_LINE, MONTHS, TIME_FORMAT,
                             TIME_SHIFT_FOR_LINE, TYPE_HOLIDAY, TYPE_SHIFTS)

PATH_TO_FILE = f"{settings.BASE_DIR}/data_files/work_shifts.xlsx"


class Command(BaseCommand):
    """Команда python manage.py parse название линии тип """
    help = "Команда парсинга графика/отпуска"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "line",
            type=str,
            help=(
                "Необходимо указать парсинг какой линии требуется "
                "first, second, gsma"
            )
        )
        parser.add_argument(
            "type_parse",
            type=str,
            help=(
                "Тип парсинга: shifts - смены |"
                " holidays - отпуск | all - все"
            )
        )

    def handle(self, *args, **kwargs) -> None:
        type_parse: str = kwargs["type_parse"]
        line: str = kwargs["line"]
        try:
            match line:
                case "second" | "first" | "gsma":
                    return self.parse_line(
                        type_parse=type_parse,
                        type_line=line
                    )
                case _:
                    text = (
                        "Неизвестная команда!\n"
                        "Используй first, second или gsma"
                    )
                    return self.bad(txt=text)
        except ValueError as e:
            return self.bad(txt=str(e))

    def parse_line(self, type_parse: str, type_line: str) -> None:
        match type_parse:
            case "shifts":
                parse_work_shifts(type_line=type_line)
            case "holidays":
                parse_holidays(type_line=type_line)
            case "all":
                parse_work_shifts(type_line=type_line)
                parse_holidays(type_line=type_line)
            case _:
                text = (
                    "Неизвестная команда!\n"
                    "Используй shifts, holidays или all"
                )
                return self.bad(txt=text)
        return self.success()

    def success(self) -> None:
        self.stdout.write(
            self.style.SUCCESS('Данные из файла загружены')
        )

    def bad(self, txt: str) -> None:
        self.stdout.write(
            self.style.ERROR(txt)
        )


def open_wb() -> Workbook:
    month, year = timezone.now().strftime('%B %Y').split(" ", 1)
    period = f"{MONTHS.get(month)} {year}"

    try:
        wb = load_workbook(filename=PATH_TO_FILE)
    except FileNotFoundError as e:
        raise ValueError(str(e))
    except InvalidFileException as e:
        return ValueError(str(e))

    try:
        sheet = wb[period]
    except KeyError as e:
        raise ValueError(str(e))

    return sheet


def parse_work_shifts(type_line: str) -> bool:
    try:
        sheet = open_wb()
    except ValueError as e:
        raise ValueError(f"При обработке файла возникла ошибка: {e}")

    column_start, column_end = COLUMN_FOR_LINE.get(type_line)

    for cell in range(column_start, column_end):
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
                        f"Необходимо проверить исходные данные\n"
                        f"Ошибка при парсинге смен.\n"
                        f"Ячейка {data[cell]}"
                    )
                try:
                    user = User.objects.get(
                        last_name=last_name,
                        first_name=first_name
                    )
                except user.DoesNotExist:
                    raise ValueError(
                        f"Сотрудника {last_name} {first_name} нет в базе.\n"
                        f"Вероятно нужно добавить или "
                        f"допущена ошибка в имени/фамилии."
                        f"Ячейка {data[cell]}"
                    )
                if cell in [9, 10]:
                    time = data[
                        TIME_SHIFT_FOR_LINE.get(type_line)[1]
                    ].value
                else:
                    time = (
                        data[TIME_SHIFT_FOR_LINE.get(type_line)].value
                        if type_line != "first"
                        else data[
                            TIME_SHIFT_FOR_LINE.get(type_line)[0]
                        ].value
                    )
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
                        WorkShifts.objects.get_or_create(
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
                            f"{date}, {prepare_time}, {user}"
                        )


def parse_holidays(type_line: str) -> bool:
    try:
        sheet = open_wb()
    except ValueError as e:
        raise ValueError(f"При обработке файла возникла ошибка: {e}")

    column_start, column_end = COLUMN_FOR_LINE.get(type_line)

    for cell in range(column_start, column_end):
        for data in sheet:
            data_cell = data[cell].value
            if isinstance(data_cell, datetime):
                date = data_cell.date()
            elif data[HOLIDAY_FOR_LINE.get(type_line)].value == "Отпуск":
                if data_cell is not None and data_cell != "-":
                    try:
                        last_name, first_name = data_cell.split(" ", 1)
                    except Exception as e:
                        raise ValueError(
                            f"При обработке файла возникла ошибка: {e}\n"
                            f"Необходимо проверить исходные данные\n"
                            f"Ошибка при парсинге отпуска.\n"
                            f"Ячейка {data[cell]}"
                        )
                    try:
                        user = User.objects.get(
                            last_name=last_name,
                            first_name=first_name
                        )
                    except user.DoesNotExist:
                        raise ValueError(
                            f"Сотрудника {last_name} {first_name} нет в базе.\n"
                            f"Вероятно нужно добавить или "
                            f"допущена ошибка в имени/фамилии.\n"
                            f"Ячейка {data[cell]}"
                        )
                    # Пока что только мешает установка статуса
                    # Ставлю для всех Запланирован
                    # Потом надо решить, что делать с ними
                    # if timezone.now().date() < date:
                    #     status = "Запланирован"
                    # else:
                    #     status = "Завершен"
                    status = CHOICES_STATUS_HOLIDAY[0][0]
                    try:
                        Holiday.objects.get_or_create(
                            employee=user,
                            date=date,
                            status=status,
                            type=TYPE_HOLIDAY.get("yearly")
                        )
                    except Exception as e:
                        raise ValueError(
                            f"При записи отпуска возникла ошибка {e}\n"
                            f"Входные данные: {user}, {date}, {status}"
                        )


def preparation_time(
        time, time_start, time_end
) -> dict[str, str | datetime]:

    night_shift = False
    type = ""

    if time_start.startswith("21:00"):
        night_shift = True

    if (
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
    }
