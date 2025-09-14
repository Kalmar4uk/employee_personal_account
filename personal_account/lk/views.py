import hashlib

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.serializers import serialize
from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from lk.models import WorkShifts
from users.models import GroupJob
from utils.constants import CURRENT_MONTH


def create_token(username):
    str_for_hash = (
        f"{username}"
        f"{settings.SECRET_KEY_FOR_REQUEST}"
    ).encode("utf-8")
    token = hashlib.sha256(str_for_hash).hexdigest()
    return token


def check_token(func):
    def wrapper(request):
        username = request.GET.get("username")
        token = request.GET.get("token")

        if not token or token != create_token(username):
            return JsonResponse({"responce": "Forbidden"}, status=403)
        return func(request)
    return wrapper


def auth_for_token(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    if not username or not password:
        return JsonResponse(
            {
                "responce": "Не переданы username и/или пароль"
            },
            status=401
        )

    user = authenticate(username=username, password=password)

    if not user:
        return JsonResponse(
            {
                "responce": "Некорректный username или пароль"
            },
            status=401
        )

    token = create_token(username)

    return JsonResponse({"token": token})


@check_token
def shifts(request):
    groups = GroupJob.objects.all().prefetch_related("users")
    result = [
        {
            "title": group.title,
            "employees": [
                {
                    "first_name": employee.first_name,
                    "last_name": employee.last_name,
                    "work_shifts": [
                        {
                            "date_start": work_shift.date_start,
                            "date_end": work_shift.date_end,
                            "time_start": work_shift.time_start,
                            "time_end": work_shift.time_end,
                            "night_shift": work_shift.night_shift,
                        } for work_shift in employee.workshifts.filter(
                            date_start__month__gte=CURRENT_MONTH
                        )
                    ]
                } for employee in group.users.all().prefetch_related(
                    "workshifts"
                )
            ]
        } for group in groups
    ]
    return JsonResponse({"result": result}, safe=False)
