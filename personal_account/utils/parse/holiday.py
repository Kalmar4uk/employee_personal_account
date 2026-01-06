from datetime import datetime

from django.utils import timezone

from lk.models import Holiday
from users.models import User
from utils.constants import (CHOICES_STATUS_HOLIDAY, COLUMN_FOR_LINE,
                             DATE_FORMAT, HOLIDAY_FOR_LINE, MONTH_NAME,
                             RMONTHS, TYPE_HOLIDAY)
from utils.parse.parse import open_wb


def parse_holidays_gsma(file: any) -> bool:
    try:
        sheet = open_wb(file=file, holiday_gsma=True)
    except ValueError as e:
        raise ValueError(f"При обработке файла возникла ошибка: {e}")

    year = timezone.now().year + 1

    dates = []

    for col in sheet:
        for cell in col:
            if cell.value in MONTH_NAME:
                month = RMONTHS[cell.value]
            if cell.fill.fgColor.rgb == "FF92D050":
                date_str = f"{year}-{month}-{cell.value}"
                dates.append(datetime.strptime(date_str, DATE_FORMAT))
                user_data = col[7].value
        if dates:
            user_data = col[7].value
            if "/" in user_data:
                users = user_data.split("/", 1)
                for user in users:
                    for_create_holiday(user, dates)
            else:
                for_create_holiday(user_data, dates)
        dates.clear()
    return True


def for_create_holiday(user: str, dates: list[datetime]):
    last_name, first_name = user.strip().split(" ", 1)
    employee = User.objects.get(first_name=first_name, last_name=last_name)
    Holiday.objects.bulk_create(
        Holiday(
            employee=employee,
            date=date,
            status="status",
            type=TYPE_HOLIDAY.get("yearly")
        ) for date in dates
    )


def parse_holidays(file: any, type_line: str) -> bool:
    try:
        sheet = open_wb(file=file)
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
                    except User.DoesNotExist:
                        raise ValueError(
                            f"Сотрудника {last_name} {first_name} "
                            f"нет в базе.\n"
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
    return True
