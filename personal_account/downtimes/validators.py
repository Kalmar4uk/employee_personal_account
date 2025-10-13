from django.utils import timezone
from django.core.exceptions import ValidationError


def check_date(value):
    if value < timezone.now():
        raise ValidationError("Уже поздно добавлять или ошибся с датой")
