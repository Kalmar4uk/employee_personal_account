from django import forms

from downtimes.models import Downtime, ReminderDowntime


class DowntimeForm(forms.ModelForm):
    start_first_reminder = forms.DateTimeField(
        label="Время первого напоминания",
        required=False,
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M',
            attrs={'type': 'datetime-local'}
        ),
        help_text=(
            "*Данное поле необязательно, "
            "если не указать будут установлены "
            "стандартные значения напоминания"
        )
    )

    class Meta:
        model = Downtime
        fields = (
            "service",
            "start_downtime",
            "end_downtime",
            "link_task",
            "description"
        )
        widgets = {
            "start_downtime": forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
                attrs={'type': 'datetime-local'}
            ),
            "end_downtime": forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
                attrs={'type': 'datetime-local'}
            ),
            "description": forms.Textarea(
                attrs={"row": 5, "col": 20}
            )
        }


class ReminderDowntimeForm(forms.ModelForm):

    class Meta:
        model = ReminderDowntime
        fields = ("first_reminder",)
        widgets = {
            "first_reminder": forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
                attrs={'type': 'datetime-local'}
            )
        }
