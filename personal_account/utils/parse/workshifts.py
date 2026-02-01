from datetime import datetime, timedelta

from lk.models import WorkShifts
from users.models import User
from utils.constants import (COLUMN_FOR_LINE, CURRENT_MONTH, LINE_JOB,
                             TIME_SHIFT_FOR_LINE, TYPE_SHIFT_FOR_LINE)
from utils.parse.parse import open_wb, preparation_time, preparation_type_shift


def parse_work_shifts(type_line: str, file: any) -> bool:
    try:
        sheet = open_wb(file=file)
    except ValueError as e:
        raise ValueError(f"При обработке файла возникла ошибка: {e}")

    column_start, column_end = COLUMN_FOR_LINE.get(type_line)

    WorkShifts.objects.filter(
        employee__group_job=LINE_JOB.get(type_line),
        date_start__month=CURRENT_MONTH
    ).delete()

    result_for_save = []

    for cell in range(column_start, column_end):
        for data in sheet:
            shift: str | None = data[cell].value
            if isinstance(shift, datetime):
                date = shift.date()
            elif shift != "-" and shift is not None:
                if date.month == CURRENT_MONTH:
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
                            last_name=last_name.strip(),
                            first_name=first_name.strip()
                        )
                    except User.DoesNotExist:
                        raise ValueError(
                            f"Сотрудника {last_name} {first_name} "
                            f"нет в базе.\n"
                            f"Вероятно нужно добавить или "
                            f"допущена ошибка в имени/фамилии."
                            f"Ячейка {data[cell]}"
                        )
                    type_shift = data[TYPE_SHIFT_FOR_LINE.get(type_line)].value
                    prepare_type_shift = preparation_type_shift(type_shift)

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
                            time_start, time_end = time.strip().split("-", 1)
                        except Exception as e:
                            raise ValueError(
                                f"При обработке файла возникла ошибка: {e}\n"
                                f"Необходимо проверить исходные данные\n"
                                f"Ошибка при парсинге времени.\n"
                                f"Ячейка {data[cell]}"
                            )
                        prepare_time = preparation_time(
                            time_start=time_start.strip(),
                            time_end=time_end.strip()
                        )
                        result_for_save.append(
                            WorkShifts(
                                employee=user,
                                date_start=date,
                                date_end=(
                                    date+timedelta(days=1)
                                    if prepare_type_shift.get("night_shift")
                                    else date
                                ),
                                time_start=prepare_time.get("time_start"),
                                time_end=prepare_time.get("time_end"),
                                night_shift=prepare_type_shift.get(
                                    "night_shift"
                                ),
                                type=prepare_type_shift.get("type")
                            )
                        )
    try:
        WorkShifts.objects.bulk_create(result_for_save)
    except Exception as e:
        raise ValueError(
            f"При записи смен возникла ошибка {e}"
        )

    return True
