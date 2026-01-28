import uuid

from django.db import models

from downtimes.validators import check_date
from users.models import User


class Downtime(models.Model):
    service = models.CharField("Сервис", max_length=50)
    start_downtime = models.DateTimeField(
        "Дата и время начала работ",
        validators=(check_date,)
    )
    end_downtime = models.DateTimeField(
        "Дата и время окончания работ",
        validators=(check_date,)
    )
    gsma_employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="downtimes",
        verbose_name="Сотрудник от ГСМАиЦП"
    )
    link_task = models.URLField("Ссылка на задачу", max_length=150)
    description = models.CharField("Описание", max_length=500)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="downtimes_author",
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(
        "Дата создания записи",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Проведение работ на сервисе"
        verbose_name_plural = "Проведение работ на сервисе"
        ordering = ("-start_downtime",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gsma_employee",
                    "service",
                    "start_downtime",
                    "end_downtime"
                ],
                name='unique_downtime'
            )
        ]

    def __str__(self):
        return f"Проведение работ на сервисе {self.service}"


class ReminderDowntime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    downtime = models.OneToOneField(
        Downtime,
        verbose_name="Плановая работа",
        on_delete=models.CASCADE,
        related_name="reminder_downtime"
    )
    first_reminder = models.DateTimeField("Первое уведомление")
    second_reminder = models.DateTimeField(
        "Второе уведомление",
        null=True,
        blank=True
    )
    success_reminder = models.BooleanField(
        "Уведомления отправлено в Redis",
        default=False
    )
    created_at = models.DateTimeField("Создано от", auto_now_add=True)

    class Meta:
        verbose_name = "Напоминание по проведению работ"
        verbose_name_plural = "Напоминания по проведению работ"

    def __str__(self):
        return f"Уведомления по плановой работе {self.downtime}"
