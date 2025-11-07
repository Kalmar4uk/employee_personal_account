from datetime import date

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   extend_schema)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.filters import DowntimeDatesFilter
from api.permissions import BotOrStandartPermissions
from api.serializers import CreateAndUpdateSerializer, DowntimeSerializer
from downtimes.models import Downtime


class DowntimeViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Downtime.objects.all()
    serializer_class = DowntimeSerializer
    permission_classes = (BotOrStandartPermissions,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DowntimeDatesFilter
    pagination_class = None
    http_method_names = ("get", "post", "put")

    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset
        return Downtime.objects.filter(start_downtime__gte=timezone.now())

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == "PUT":
            return CreateAndUpdateSerializer
        return DowntimeSerializer

    @extend_schema(
            responses={
                200: DowntimeSerializer,
                404: OpenApiResponse(
                    response=None,
                    description="Downtime not found"
                ),
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение downtime по его id",
            tags=["Downtime"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
            responses={
                200: DowntimeSerializer,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение всех downtimes",
            tags=["Downtime"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
            request=CreateAndUpdateSerializer,
            responses={
                201: DowntimeSerializer,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
                422: OpenApiResponse(
                    response=None,
                    description="Unprocessable Entity"
                ),
            },
            summary="Создание downtime",
            tags=["Downtime"]
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateAndUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
            request=CreateAndUpdateSerializer,
            responses={
                201: DowntimeSerializer,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
                404: OpenApiResponse(
                    response=None,
                    description="Not found"
                ),
                422: OpenApiResponse(
                    response=None,
                    description="Unprocessable Entity"
                )
            },
            summary="Обновление downtime по его id",
            tags=["Downtime"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
            responses={
                200: DowntimeSerializer(many=True),
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            parameters=[
                OpenApiParameter(
                    name="start_from",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=date
                ),
                OpenApiParameter(
                    name="start_to",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=date
                ),
                OpenApiParameter(
                    name="end_from",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=date
                ),
                OpenApiParameter(
                    name="end_to",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=date
                )
            ],
            summary="Получение прошедших downtimes",
            tags=["Downtime"]
    )
    @action(detail=False, url_path="old")
    def get_old_downtime(self, request):
        queryset = Downtime.objects.filter(end_downtime__lte=timezone.now())
        filtered_queryset = self.filter_queryset(queryset)
        self.pagination_class = PageNumberPagination

        serializer = self.get_serializer(
            filtered_queryset,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class DowntimeViewSetV2(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Downtime.objects.all()
    serializer_class = DowntimeSerializer
    permission_classes = (BotOrStandartPermissions,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DowntimeDatesFilter
    pagination_class = None
    http_method_names = ("get", "post", "put")

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        pass

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        pass

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        pass

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        pass

    @extend_schema(
            responses={
                200: DowntimeSerializer(many=True),
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            parameters=[
                OpenApiParameter(
                    name="start_from",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=date
                ),
                OpenApiParameter(
                    name="start_to",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=date
                ),
                OpenApiParameter(
                    name="end_from",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=date
                ),
                OpenApiParameter(
                    name="end_to",
                    location=OpenApiParameter.QUERY,
                    required=False,
                    type=date
                )
            ],
            description=(
                "Добавлена пагинация для ответа. "
                "10 записей за раз"
            ),
            summary="Получение прошедших downtimes",
            tags=["Downtime"]
    )
    @action(
        detail=False,
        url_path="old",
        pagination_class=PageNumberPagination
    )
    def get_old_downtime(self, request):
        queryset = Downtime.objects.filter(end_downtime__lte=timezone.now())
        filtered_queryset = self.filter_queryset(queryset)
        self.pagination_class = PageNumberPagination

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            filtered_queryset,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
