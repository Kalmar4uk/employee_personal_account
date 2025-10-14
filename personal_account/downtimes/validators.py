from django.core.exceptions import ValidationError
from django.utils import timezone


def check_date(value):
    if value < timezone.now():
        raise ValidationError("Уже поздно добавлять или ошибся с датой")
