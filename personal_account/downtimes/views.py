from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from downtimes.forms import DowntimeForm
from downtimes.models import Downtime
from utils.functions import get_workshift_for_downtime


@login_required
def create_downtime(request):
    form = DowntimeForm(request.POST or None)

    if form.is_valid():
        downtime = form.save()
        start_downtime = form.cleaned_data.get("start_downtime")
        shifts = get_workshift_for_downtime(start_downtime=start_downtime)
        downtime.gsma_employee = shifts.employee
        downtime.save()
        return redirect(reverse("downtimes:downtime"))

    context = {"form": form}

    return render(request, "downtime/added_downtime.html", context)


@login_required
def downtimes(request):
    downtimes = Downtime.objects.filter(start_downtime__gte=timezone.now())
    context = {"downtimes": downtimes}
    return render(request, "downtime/downtime.html", context)


@login_required
def downtimes_detail(request, id):
    downtime = get_object_or_404(Downtime, id=id)
    context = {"downtime": downtime}
    return render(request, "downtime/downtime_detail.html", context)


@login_required
def edit_downtimes(request, id):
    downtime = get_object_or_404(Downtime, id=id)

    form = DowntimeForm(request.POST or None, instance=downtime)

    if form.is_valid():
        form.save()
        return redirect(
            reverse(
                "downtimes:downtime_detail",
                kwargs={"id": downtime.id}
            )
        )

    context = {
        "form": form,
        "downtime": downtime
    }

    return render(request, "downtime/added_downtime.html", context)


@login_required
def history_downtimes(request):
    downtimes = Downtime.objects.filter(start_downtime__lt=timezone.now())
    context = {"downtimes": downtimes}
    return render(request, "downtime/history_downtime.html", context)
