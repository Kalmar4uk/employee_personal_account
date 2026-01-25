from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from downtimes.forms import DowntimeForm, ReminderDowntimeForm
from downtimes.models import Downtime, ReminderDowntime
from downtimes.push_downtime import created_send_downtime
from utils.functions import (check_time_downtime_and_first_reminder,
                             get_workshift_for_downtime)


@login_required
def create_downtime(request):
    form = DowntimeForm(request.POST or None)

    if form.is_valid():
        start_downtime = form.cleaned_data.get("start_downtime")
        start_reminder_downtime = form.cleaned_data.pop("start_first_reminder")
        try:
            shifts = get_workshift_for_downtime(start_downtime=start_downtime)
        except ValueError as e:
            return render(
                request,
                "errors/400.html",
                context={"error": e},
                status=400
            )

        downtime = form.save(commit=False)
        downtime.gsma_employee = shifts.employee
        downtime.author = request.user
        downtime.save()

        if start_reminder_downtime:

            if not check_time_downtime_and_first_reminder(
                downtime.start_downtime,
                downtime.end_downtime,
                start_reminder_downtime
            ):
                return render(
                    request,
                    "errors/incorrect_reminder.html",
                    context={"downtime": downtime}
                )

            ReminderDowntime.objects.create(
                downtime=downtime,
                first_reminder=start_reminder_downtime,
                second_reminder=(downtime.start_downtime - timedelta(hours=1))
            )
        else:
            ReminderDowntime.objects.create(
                downtime=downtime,
                first_reminder=(downtime.start_downtime - timedelta(hours=5)),
                second_reminder=(downtime.start_downtime - timedelta(hours=1))
            )

        created_send_downtime(downtine=downtime)

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
    reminder_downtime = downtime.reminder_downtime
    context = {"downtime": downtime, "reminder_downtime": reminder_downtime.id}
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


@login_required
def edit_reminder_downtimes(request, id, reminder_id):
    form = ReminderDowntimeForm(request.POST or None)
    downtime = get_object_or_404(Downtime, id=id)

    if form.is_valid():
        first_reminder = form.cleaned_data.get("first_reminder")
        if not check_time_downtime_and_first_reminder(
            downtime.start_downtime,
            downtime.end_downtime,
            first_reminder
        ):
            return render(
                request,
                "errors/400.html",
                context={"error": "Некорректное время напоминания"},
                status=400
            )

        ReminderDowntime.objects.filter(
            id=reminder_id
        ).update(
            first_reminder=first_reminder
        )

        return redirect(
            reverse(
                "downtimes:downtime_detail",
                kwargs={"id": id}
            )
        )

    context = {
        "form": form,
        "downtime": downtime
    }

    return render(request, "downtime/edit_reminder_downtime.html", context)
