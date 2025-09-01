from django.db import models
from django.contrib.auth.models import AbstractUser
from users.manager import CustomUserManager


class User(AbstractUser):
    email = models.EmailField("Email", unique=True)
    job_title = models.CharField("Должность", max_length=100)
    personnel_number = models.CharField(
        "Табельный номер",
        max_length=20,
        unique=True
    )
    group_job = models.ManyToManyField(
        "GroupJob",
        verbose_name="Группа сотрудника",
        related_name="users"
    )
    is_main = models.BooleanField("Босс этой качалки", default=False)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.is_active is False and not self.email.startswith("Not"):
            self.email = f"Not active - {self.email}"
        self.username, _ = self.email.rsplit("@", 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class GroupJob(models.Model):
    title = models.CharField("Название", max_length=100, unique=True)

    class Meta:
        verbose_name = "Рабочая группа"
        verbose_name_plural = "Рабочие группы"

    def __str__(self):
        return self.title
