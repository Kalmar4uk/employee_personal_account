from api.serializers import (GroupJobSerializer, ListGroupsJobSerializer,
                             UsersSerializer, UsersSerializerV2)
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import GroupJob, User


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    @extend_schema(
            responses={
                200: UsersSerializer,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение текущего сотрудника",
            tags=["Users"]
    )
    @action(detail=False, url_path="me")
    def get_me(self, request):
        serializer = UsersSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
            responses={
                200: UsersSerializer,
                404: OpenApiResponse(
                    response=None,
                    description="User not found"
                ),
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение сотрудника по его id",
            tags=["Users"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
            responses={
                200: UsersSerializer,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение всех сотрудников",
            tags=["Users"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserViewSetV2(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UsersSerializerV2

    @extend_schema(
            responses={
                200: UsersSerializerV2,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение текущего сотрудника",
            tags=["Users"]
    )
    @action(detail=False, url_path="me")
    def get_me(self, request):
        serializer = UsersSerializerV2(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
            responses={
                200: UsersSerializerV2,
                404: OpenApiResponse(
                    response=None,
                    description="User not found"
                ),
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение сотрудника по его id",
            tags=["Users"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
            responses={
                200: UsersSerializerV2,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение всех сотрудников",
            tags=["Users"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GroupJobViewSet(viewsets.ModelViewSet):
    queryset = GroupJob.objects.all()
    http_method_names: list[str] = ["get"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListGroupsJobSerializer
        return GroupJobSerializer

    @extend_schema(
            responses={
                200: GroupJobSerializer,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение группы по id",
            tags=["Groups"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
            responses={
                200: ListGroupsJobSerializer,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение списка групп",
            tags=["Groups"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
