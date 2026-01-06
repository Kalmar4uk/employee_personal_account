from datetime import datetime, timedelta

from lk.models import WorkShifts
from users.models import User
from utils.constants import COLUMN_FOR_LINE, TIME_SHIFT_FOR_LINE
from utils.parse.parse import open_wb, preparation_time


def parse_work_shifts(type_line: str, file: any) -> bool:
    try:
        sheet = open_wb(file=file)
    except ValueError as e:
        raise ValueError(f"При обработке файла возникла ошибка: {e}")

    column_start, column_end = COLUMN_FOR_LINE.get(type_line)

    for cell in range(column_start, column_end):
        for data in sheet:
            shift: str | None = data[cell].value
            if isinstance(shift, datetime):
                date = shift.date()
            elif shift != "-" and shift is not None:
                if shift.isspace():
                    continue
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
                except User.DoesNotExist:
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
                if (time == "-" or time is None) and shift is not None:
                    continue
                else:
                    try:
                        time_start, time_end = time.split(" - ", 1)
                    except Exception as e:
                        raise ValueError(
                            f"При обработке файла возникла ошибка: {e}\n"
                            f"Необходимо проверить исходные данные\n"
                            f"Ошибка при парсинге времени.\n"
                            f"Ячейка {data[cell]}"
                        )
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
    return True
