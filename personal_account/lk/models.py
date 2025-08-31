from django.db import models
from users.models import User


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
    ("Ежегодный оплачиваемый отпуск", "Ежегодный оплачиваемый отпуск")
)


class WorkShiftsAndHolidayModel(models.Model):
    date_start = models.DateField(
        "Дата начала",
        null=True,
        blank=True
    )
    date_end = models.DateField(
        "Дата окончания",
        null=True,
        blank=True
    )
    time_start = models.TimeField("Время начала", null=True, blank=True)
    time_end = models.TimeField("Время окончания", null=True, blank=True)

    class Meta:
        abstract = True


class WorkShifts(WorkShiftsAndHolidayModel):
    employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сотрудник",
        related_name="workshifts"
    )
    type = models.CharField(
        "Тип графика",
        max_length=7,
        choices=CHOICES_TYPE_WORK_SHIFT
    )
    night_shift = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"

    def __str__(self):
        return f"Смена {self.employee}"


class Holiday(WorkShiftsAndHolidayModel):
    employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="holidays"
    )
    type = models.CharField(
        "Тип отпуска",
        max_length=50,
        choices=CHOICES_TYPE_HOLIDAY
    )
    status = models.CharField(
        "Статус",
        max_length=15,
        choices=CHOICES_STATUS_HOLIDAY
    )
    count_day = models.PositiveSmallIntegerField("Кол-во дней")

    class Meta:
        verbose_name = "Отпуск"
        verbose_name_plural = "Отпуска"

    def save(self, *args, **kwargs):
        days = self.date_end - self.date_start
        self.count_day = days.days + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Отпуск {self.employee}"
