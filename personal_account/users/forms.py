from django import forms
from django.core.exceptions import ValidationError

from users.models import User


class MySetPassword(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=8)

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not User.objects.filter(username=data).exists():
            raise ValidationError("Неверно введен логин")
        return data
