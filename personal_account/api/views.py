from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import (BlacklistedToken,
                                                             OutstandingToken)
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import (CalendarSerializer, GroupJobSerializer,
                             HolidaysSerializer, ListGroupsJobSerializer,
                             TokenSerializer, UsersSerializer,
                             WorkShiftsSerializer)
from users.models import GroupJob, User
from utils.functions import days_current_month


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

    @action(detail=True, url_path="calendar")
    def get_calendar_user(self, request, pk):
        user = get_object_or_404(User, id=pk)
        dates = days_current_month()
        calendar = []
        for date in dates:
            work = user.workshifts.filter(date_start=date).first()
            holiday = user.holidays.filter(date=date).first()
            if work:
                calendar.append(
                    {
                        "date": date.date(),
                        "type": "shifts",
                        "time": (
                            f"{work.time_start.strftime('%H:%M')} - "
                            f"{work.time_end.strftime('%H:%M')}"
                        )
                    }
                )
            elif holiday:
                calendar.append(
                    {
                        "date": date.date(),
                        "type": "holiday",
                        "time": "Отпуск"
                    }
                )
            else:
                calendar.append(
                    {
                        "date": date.date(),
                        "type": "day-off",
                        "time": "Выходной"
                    }
                )
        serializer = CalendarSerializer(
            calendar,
            context={"request": request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupJobViewSet(viewsets.ModelViewSet):
    queryset = GroupJob.objects.all()
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListGroupsJobSerializer
        return GroupJobSerializer
