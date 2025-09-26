from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import (BlacklistedToken,
                                                             OutstandingToken)
from rest_framework_simplejwt.tokens import RefreshToken

from api.functions import get_calendar, get_group_calendar
from api.permissions import ForBotRequestPermission
from api.serializers import (GroupJobSerializer, ListGroupsJobSerializer,
                             TokenSerializer, UserCalendarSerializer,
                             UsersSerializer)
from users.models import GroupJob, User
from utils.constants import CURRENT_MONTH


class APIToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = get_object_or_404(User, email=email)
        refresh = RefreshToken.for_user(user)
        refresh.payload.update(
            {
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        )
        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            },
            status=status.HTTP_201_CREATED
        )


class DeleteAPIToken(APIView):

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    @action(detail=False, url_path="me")
    def get_me(self, request):
        serializer = UsersSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupJobViewSet(viewsets.ModelViewSet):
    queryset = GroupJob.objects.all()
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListGroupsJobSerializer
        return GroupJobSerializer


class DataForBot(APIView):
    permission_classes = (ForBotRequestPermission,)

    def get(self, request):
        groups = GroupJob.objects.all().prefetch_related("users")
        try:
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


class CalendarView(APIView):

    def get(self, request):
        user_id = self.request.query_params.get("user")
        group_id = self.request.query_params.get("group")

        if user_id:
            user = get_object_or_404(User, id=user_id)
            result = {"user": user.id, "calendar": get_calendar(user=user)}
            serializer = UserCalendarSerializer(
                result,
                context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        if group_id:
            group = get_object_or_404(GroupJob, id=group_id)
            result = get_group_calendar(group=group)
            serializer = UserCalendarSerializer(
                result,
                context={"request": request},
                many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {
                "not_found": (
                    "Отсутствуют query параметры или переданы неизвестные"
                )
            },
            status=status.HTTP_400_BAD_REQUEST
        )
