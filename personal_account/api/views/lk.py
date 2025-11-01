from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.functions import get_calendar, get_group_calendar
from api.serializers import UserCalendarSerializer
from users.models import GroupJob, User


class CalendarView(viewsets.ViewSet):
    queryset = User.objects.all()

    @extend_schema(
            responses={
                200: UserCalendarSerializer
            },
            parameters=[
                OpenApiParameter(
                    name="month",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=str
                ),
                OpenApiParameter(
                    name="year",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=str
                )
            ],
            summary="Получение рабочего календаря для сотрудника",
            description="По умолчанию отдает календарь за текущий месяц и год",
            tags=["Calendar"]
    )
    def user(self, request, user_id):
        month: int = int(self.request.query_params.get("month", 0))
        year: int = int(self.request.query_params.get("year", 0))

        user = get_object_or_404(User, id=user_id)
        result: dict[str] = {
            "user": user.id,
            "calendar": get_calendar(user=user, month=month, year=year)
        }
        serializer = UserCalendarSerializer(
            result,
            context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
            responses={
                200: UserCalendarSerializer(many=True)
            },
            parameters=[
                OpenApiParameter(
                    name="month",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=str
                ),
                OpenApiParameter(
                    name="year",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=str
                )
            ],
            summary="Получение рабочего календаря для сотрудников группы",
            description="По умолчанию отдает календарь за текущий месяц и год",
            tags=["Calendar"]
    )
    def group(self, request, group_id):
        month: int = int(self.request.query_params.get("month", 0))
        year: int = int(self.request.query_params.get("year", 0))
        group = get_object_or_404(GroupJob, id=group_id)
        result = get_group_calendar(group=group, month=month, year=year)
        serializer = UserCalendarSerializer(
            result,
            context={"request": request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
