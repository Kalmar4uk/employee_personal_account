from django.db import models
from users.models import User
from downtimes.validators import check_date


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
        verbose_name="Сотрудник от ГСМАиЦП"
    )
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
