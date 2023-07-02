from logging import getLogger

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ViewSet

from application.models.user import User
from application.serializers.user import LoginSerializer, UserSerializer
from application.utils.get_client_ip import get_client_ip
from application.utils.logs import LoggerName


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
        if not serializer.is_valid():
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        employee_number = serializer.validated_data.get("employee_number")
        password = serializer.validated_data.get("password")
        user = authenticate(employee_number=employee_number, password=password)
        if not user:
            self.application_logger.warning(
                f"ログイン失敗:{serializer.data.get('employee_number')}, IP: {get_client_ip(request)}"
            )
            return JsonResponse(
                data={
                    "msg": "either employee number or password is incorrect"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            login(request, user)
            self.application_logger.info(
                f"ログイン成功: {user}, {serializer.data.get('employee_number')}, IP: {get_client_ip(request)}"
            )
            return JsonResponse(data={"role": user.Role(user.role).name})

    @action(methods=["POST"], detail=False)
    def logout(self, request):
        """ログアウト"""
        self.application_logger.info(
            f"ログアウト: {request.user}, IP: {get_client_ip(request)}"
        )
        logout(request)
        return HttpResponse()
