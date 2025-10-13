from django import forms
from downtimes.models import Downtime


class DowntimeForm(forms.ModelForm):

    class Meta:
        model = Downtime
        fields = "service", "start_downtime", "end_downtime", "description"
        widgets = {
            "start_downtime": forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'type': 'datetime-local'}),
            "end_downtime": forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'type': 'datetime-local'})
        }
