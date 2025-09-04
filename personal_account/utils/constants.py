from django.utils import timezone

CURRENT_MONTH = timezone.now().month

CHOICES_TYPE_WORK_SHIFT = (
    ("Сменный", "Сменный"),
    ("5/2", "5/2")
)

CHOICES_STATUS_HOLIDAY = (
    ("Запланирован", "Запланирован"),
    ("Завершен", "Завершен"),
    ("Отменен", "Отменен")
)

CHOICES_TYPE_HOLIDAY = (
    ("Отпуск без сохранения заработной платы", (
        "Отпуск без сохранения заработной платы"
    )),
    ("Ежегодный оплачиваемый", "Ежегодный оплачиваемый")
)

TIME_FORMAT = "%H:%M"

TYPE_HOLIDAY = {
    "yearly": "Ежегодный оплачиваемый",
    "without_pay": "Без сохранения заработной платы"
}

TYPE_SHIFTS = {"schedule": "Сменный", "standart": "5/2"}

COLUMN_FOR_GSMA = [26, 33]
TIME_SHIFT_FOR_GSMA = 24
HOLIDAY_FOR_GSMA = 23

COLUMN_FOR_FL = [4, 11]
TIME_SHIFT_DAY_FOR_FL = 2
TIME_SHIFT_FOR_NIGHT_FL = 3
HOLIDAY_FOR_FL = 1

COLUMN_FOR_SL = [15, 22]
TIME_SHIFT_FOR_SL = 13
HOLIDAY_FOR_SL = 12

COLUMN_FOR_LINE = {
    "first": COLUMN_FOR_FL,
    "second": COLUMN_FOR_SL,
    "gsma": COLUMN_FOR_GSMA
}

TIME_SHIFT_FOR_LINE = {
    "first": [TIME_SHIFT_DAY_FOR_FL, TIME_SHIFT_FOR_NIGHT_FL],
    "second": TIME_SHIFT_FOR_SL,
    "gsma": TIME_SHIFT_FOR_GSMA
}

HOLIDAY_FOR_LINE = {
    "first": HOLIDAY_FOR_FL,
    "second": HOLIDAY_FOR_SL,
    "gsma": HOLIDAY_FOR_GSMA
}
