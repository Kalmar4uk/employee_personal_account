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
    description = models.TextField("Описание")
    created_at = models.DateTimeField(
        "Дата создания записи",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Проведение работ на сервисе"
        verbose_name_plural = "Проведение работ на сервисе"

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
