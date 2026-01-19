from django.utils import timezone

CURRENT_MONTH = timezone.now().month
CURRENT_YEAR = timezone.now().year
CURRENT_DATE = timezone.now().date()

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
DATE_FORMAT = "%Y-%m-%d"

TYPE_HOLIDAY = {
    "yearly": "Ежегодный оплачиваемый",
    "without_pay": "Без сохранения заработной платы"
}

TYPE_SHIFTS = {"schedule": "Сменный", "standart": "5/2"}

LINE_JOB = {
    "gsma": 1,
    "first": 2,
    "second": 3
}

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

MONTHS = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
}

RMONTHS = {
    "Январь": 1,
    "Февраль": 2,
    "Март": 3,
    "Апрель": 4,
    "Май": 5,
    "Июнь": 6,
    "Июль": 7,
    "Август": 8,
    "Сентябрь": 9,
    "Октябрь": 10,
    "Ноябрь": 11,
    "Декабрь": 12
}

MONTH_NAME = [value for value in MONTHS.values()]
