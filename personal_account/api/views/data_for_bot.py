from api.permissions import ForBotRequestPermission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import GroupJob
from utils.constants import CURRENT_MONTH
from django.utils import timezone
from downtimes.models import Downtime
from datetime import timedelta
from rest_framework.permissions import AllowAny
from api.serializers import DowntimeSerializer


class DataForBot(APIView):
    permission_classes = (ForBotRequestPermission,)

    def get(self, request):
        groups = GroupJob.objects.all().prefetch_related("users")
        try:
            result: list[dict[str]] = [
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
                                    date_start__month=CURRENT_MONTH
                                )
                            ],
                            "holiday": [
                                {
                                    "date": holiday.date
                                } for holiday in employee.holidays.filter(
                                    date__month=CURRENT_MONTH
                                )
                            ]
                        } for employee in group.users.all().prefetch_related(
                            "workshifts"
                        )
                    ]
                } for group in groups
            ]
        except Exception as e:
            return Response(
                {"error": e},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        return Response(result, status=status.HTTP_200_OK)


class DowntimeDataForBor(APIView):
    permission_classes = (ForBotRequestPermission,)

    def get(self, request):
        current_date = timezone.now() + timedelta(days=1)
        downtime = Downtime.objects.filter(
            start_downtime__date=current_date.date()
        )
        serializer = DowntimeSerializer(
            downtime,
            context={"request": request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
