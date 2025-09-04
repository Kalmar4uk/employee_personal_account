from django.db import models
from users.models import User
from utils.constants import (CHOICES_STATUS_HOLIDAY, CHOICES_TYPE_HOLIDAY,
                             CHOICES_TYPE_WORK_SHIFT)


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

        constraints = [
            models.UniqueConstraint(
                fields=["date_start", "date_end", "employee"],
                name='unique_shifts'
            )
        ]

    def __str__(self):
        return f"Смена {self.employee}"


class Holiday(models.Model):
    employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сотрудник",
        related_name="holidays"
    )
    date = models.DateField(
        "Дата",
        null=True,
        blank=True
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

    class Meta:
        verbose_name = "Отпуск"
        verbose_name_plural = "Отпуска"
        ordering = ("date",)

        constraints = [
            models.UniqueConstraint(
                fields=["date", "employee"],
                name='unique_holidays'
            )
        ]

    def __str__(self):
        return f"Отпуск {self.employee}"
