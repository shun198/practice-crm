from logging import getLogger

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ViewSet

from application.models.user import User
from application.serializers.user import LoginSerializer, UserSerializer
from application.utils.logs import LoggerName
from project.settings.environment import django_settings


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    application_logger = getLogger(LoggerName.APPLICATION.value)
    emergency_logger = getLogger(LoggerName.EMERGENCY.value)

    @action(detail=False, methods=["POST"])
    def login(self, request):
        """ユーザのログイン"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee_number = serializer.validated_data.get("employee_number")
        password = serializer.validated_data.get("password")
        user = authenticate(employee_number=employee_number, password=password)
        if not user:
            return JsonResponse(
                data={"msg": "社員番号またはパスワードが間違っています"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            login(request, user)
            return JsonResponse(
                data={"username": user.username, "group": user.group.name}
            )

    @action(methods=["POST"], detail=False)
    def logout(self, request):
        """ユーザのログアウト"""
        logout(request)
        return HttpResponse()


if django_settings.DJANGO_SETTINGS_MODULE == "project.settings.local":
    from drf_spectacular.utils import (
        OpenApiExample,
        OpenApiResponse,
        extend_schema,
    )

    extend_schema(
        request=LoginSerializer,
        examples=[
            OpenApiExample(
                "ログイン",
                summary="ログインAPIのリクエスト",
                value={
                    "employee_number": "00000001",
                    "password": "test",
                },
                request_only=True,
                response_only=False,
                description="システムユーザーのログイン",
            )
        ],
        responses=OpenApiResponse(
            status.HTTP_200_OK,
            description="ログインが成功した場合",
            examples=[
                OpenApiExample(
                    "login",
                    summary={
                        "ログイン成功時のレスポンス",
                    },
                    value={"username": "管理者ユーザ01", "group": "管理者"},
                    request_only=False,
                    response_only=True,
                )
            ],
        ),
        summary="システムユーザーのログイン",
    )(LoginViewSet.login)

    extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="ログアウトに成功しました",
            ),
        },
        summary="システムユーザのログアウト",
    )(LoginViewSet.logout)
