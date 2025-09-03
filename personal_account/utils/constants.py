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
