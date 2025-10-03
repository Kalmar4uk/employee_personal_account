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
from api.serializers import (GroupJobSerializer, ListGroupsJobSerializer,
                             TokenSerializer, UserCalendarSerializer,
                             UsersSerializer, RefreshTokenSerializer)
from users.models import GroupJob, User


class APIToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email: str = serializer.validated_data.get("email")
        user = get_object_or_404(User, email=email)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            },
            status=status.HTTP_201_CREATED
        )


class APINewToken(APIView):

    def post(self, request):
        serializer = RefreshTokenSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        token_data: str = serializer.validated_data.get("refresh_token")
        token = OutstandingToken.objects.get(token=token_data)
        BlacklistedToken.objects.create(token=token)
        refresh = RefreshToken.for_user(request.user)
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
    http_method_names: list[str] = ["get"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListGroupsJobSerializer
        return GroupJobSerializer


class CalendarView(APIView):

    def get(self, request):
        user_id: str = self.request.query_params.get("user")
        group_id: str = self.request.query_params.get("group")
        month: int = int(self.request.query_params.get("month", 0))
        year: int = int(self.request.query_params.get("year", 0))

        if user_id:
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
        if group_id:
            group = get_object_or_404(GroupJob, id=group_id)
            result = get_group_calendar(group=group, month=month, year=year)
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
