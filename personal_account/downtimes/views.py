from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from downtimes.forms import DowntimeForm
from downtimes.models import Downtime
from lk.models import WorkShifts


@login_required
def added_downtime(request):
    form = DowntimeForm(request.POST or None)

    if form.is_valid():
        downtime = form.save()
        start_downtime = form.cleaned_data.get("start_downtime")
        date_start = start_downtime.date()
        shifts = WorkShifts.objects.filter(
            date_start=date_start,
            night_shift=True
        ).prefetch_related(
            "employee"
        )
        for shift in shifts:
            employee = shift.employee
            if employee.group_job.filter(id=1):
                downtime.gsma_employee = employee
                downtime.save()
                return redirect(reverse("downtimes:downtime"))

    context = {"form": form}

    return render(request, "added_downtime.html", context)


@login_required
def downtimes(request):
    downtimes = Downtime.objects.filter(start_downtime__gte=timezone.now())
    context = {"downtimes": downtimes}
    return render(request, "downtime.html", context)


@login_required
def downtimes_detail(request, id):
    downtime = get_object_or_404(Downtime, id=id)
    context = {"downtime": downtime}
    return render(request, "downtime_detail.html", context)


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

    return render(request, "added_downtime.html", context)


@login_required
def history_downtimes(request):
    downtimes = Downtime.objects.filter(start_downtime__lt=timezone.now())
    context = {"downtimes": downtimes}
    return render(request, "history_downtime.html", context)
