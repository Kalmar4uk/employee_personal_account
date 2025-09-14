from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (GroupJobSerializer, HolidaysSerializer,
                             ListGroupsJobSerializer, UsersSerializer,
                             WorkShiftsSerializer)
from users.models import GroupJob, User
from utils.constants import CURRENT_MONTH


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ["get"]

    @action(detail=True, url_path="shifts")
    def get_shifts_user(self, request, pk):
        user = User.objects.get(id=pk)
        shifts = user.workshifts.filter(
            date_start__month=CURRENT_MONTH
        ).order_by(
            "date_start"
        )
        serializer = WorkShiftsSerializer(
            shifts,
            context={"request": request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, url_path="holidays")
    def get_holiday_user(self, request, pk):
        user = User.objects.get(id=pk)
        holidays = user.holidays.filter(
            date__month=CURRENT_MONTH
        ).order_by(
            "date"
        )
        serializer = HolidaysSerializer(
            holidays,
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
