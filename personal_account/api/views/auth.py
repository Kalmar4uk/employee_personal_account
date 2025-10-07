from api.serializers import (TokenCreateSerializer, TokenSerializer,
                             UpdateTokenSerializer)
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import (BlacklistedToken,
                                                             OutstandingToken)
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class TokenView(viewsets.ViewSet):
    queryset = OutstandingToken.objects.all()

    @extend_schema(
            request=TokenCreateSerializer,
            responses={
                201: TokenSerializer,
                400: OpenApiResponse(
                    response=None,
                    description="Error validation personal data"
                )
            },
            summary="Получение токенов",
            tags=["Tokens"]
    )
    @action(
        detail=False,
        url_path="login",
        permission_classes=[AllowAny],
        methods=["post"]
    )
    def login(self, request):
        serializer = TokenCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email: str = serializer.validated_data.get("email")
        user = get_object_or_404(User, email=email)
        tokens = self.access_refresh_tokens(user=user, request=request)
        return Response(tokens, status=status.HTTP_201_CREATED)

    @extend_schema(
            request=UpdateTokenSerializer,
            responses={
                201: TokenSerializer,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
                400: OpenApiResponse(
                    response=None,
                    description="Error validation refresh token"
                )
            },
            summary="Обновление токенов",
            tags=["Tokens"]
    )
    @action(
        detail=False,
        url_path="update",
        methods=["PUT"]
    )
    def update_token(self, request):
        serializer = UpdateTokenSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        token_data: str = serializer.validated_data.get("refresh_token")
        token = OutstandingToken.objects.get(token=token_data)
        BlacklistedToken.objects.create(token=token)
        new_token = self.access_refresh_tokens(
            user=request.user,
            request=request
        )
        return Response(new_token, status=status.HTTP_201_CREATED)

    @extend_schema(
            responses={
                204: None,
                401: OpenApiResponse(
                    response=None,
                    description="No auth"
                ),
            },
            summary="Удаление токенов",
            tags=["Tokens"]
    )
    @action(
        detail=False,
        url_path="logout",
        methods=["post"]
    )
    def logout(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def access_refresh_tokens(self, user, request):
        refresh = RefreshToken.for_user(user)
        tokens: dict[str, str] = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
        serializer = TokenSerializer(tokens, context={"request": request})
        return serializer.data
