from api.permissions import BotOrStandartPermissions
from api.serializers import CreateAndUpdateSerializer, DowntimeSerializer
from django.utils import timezone
from downtimes.models import Downtime
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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

    def get_queryset(self):
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
            },
            summary="Обновление downtime по его id",
            tags=["Downtime"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
            responses={
                200: DowntimeSerializer,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Получение прошедших downtimes",
            tags=["Downtime"]
    )
    @action(detail=False, url_path="old")
    def get_old_downtime(self, request):
        queryset = Downtime.objects.filter(end_downtime__lte=timezone.now())
        serializer = DowntimeSerializer(queryset, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
