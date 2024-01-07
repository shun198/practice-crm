import secrets
from datetime import timedelta
from logging import getLogger

from django.contrib.auth import update_session_auth_hash
from django.db import DatabaseError
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from application.emails import send_invitation_email, send_reset_email
from application.models.user import User, UserInvitation, UserResetPassword
from application.permissions import IsManagementUser
from application.serializers.user import (
    ChangePasswordSerializer,
    CheckTokenSerializer,
    InviteUserSerializer,
    ResetPasswordSerializer,
    SendResetPasswordEmailSerializer,
    UserSerializer,
    VerifyUserSerializer,
)
from application.utils.logs import LoggerName
from project.settings.environment import django_settings


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    application_logger = getLogger(LoggerName.APPLICATION.value)
    emergency_logger = getLogger(LoggerName.EMERGENCY.value)

    def get_serializer_class(self):
        match self.action:
            case "change_password":
                return ChangePasswordSerializer
            case "verify_user":
                return VerifyUserSerializer
            case "invite_user":
                return InviteUserSerializer
            case "reset_password":
                return ResetPasswordSerializer
            case "check_reset_password_token" | "check_invitation_token":
                return CheckTokenSerializer
            case "send_reset_password_email":
                return SendResetPasswordEmailSerializer
            case "toggle_user_active" | "get_csrf_token" | "user_info" | "reinvite_user":
                return None
            case _:
                return UserSerializer

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "destroy",
            "partial_update",
            "send_invite_user_mail",
            "invite_user",
        }:
            permission_classes = [IsManagementUser]
        elif self.action in {
            "reset_password",
            "send_reset_password_email",
            "user_info",
        }:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def get_csrf_token(self, request):
        """CSRF Tokenを発行する

        Args:
            request (HttpRequest): HttpRequestオブジェクト

        Returns:
            JsonResponse
        """
        return JsonResponse({"token": str(get_token(request))})

    def destroy(self, request, *args, **kwargs):
        """システムユーザを削除するAPI

        Args:
            request : リクエスト

        Returns:
            Union[
                Response,
                JsonResponse
            ]
        """
        instance = self.get_object()
        if request.user == instance:
            return JsonResponse(
                data={"msg": "自身を削除する事は出来ません"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False)
    def change_password(self, request):
        """パスワードを変更するAPI

        Args:
            request : リクエスト

        Returns:
            JsonResponse
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(
            serializer.validated_data["current_password"]
        ):
            return JsonResponse(
                data={"msg": "現在のパスワードが違います"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        # sessionを更新する
        update_session_auth_hash(request, user)
        return HttpResponse()

    @action(detail=False, methods=["POST"])
    def invite_user(self, request):
        """指定したメールアドレス宛へユーザの招待メールを送る

        Args:
            request: リクエスト

        Returns:
            HttpResponse
        """
        # Userの新規登録と招待用トークンを作成する
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(
            serializer.validated_data,
            created_by=request.user,
            updated_by=request.user,
        )
        token = secrets.token_urlsafe(64)
        expiry = timezone.now() + timedelta(days=1)
        UserInvitation.objects.create(token=token, user=user, expiry=expiry)
        base_url = django_settings.BASE_URL
        # 初回登録用のURLへ遷移
        url = base_url + "/verify-user/" + token
        send_invitation_email(
            email=user.email,
            url=url,
        )
        return JsonResponse(
            data={"msg": "招待メールを送信しました"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def verify_user(self, request):
        """新規ユーザを認証する

        Args:
            request (HttpRequest): HttpRequestオブジェクト

        Returns:
            Union[
                HttpResponse,
                JsonResponse
            ]
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_invitation = self._check_invitation(serializer.data["token"])
        if user_invitation is None:
            return JsonResponse(
                data={"msg": "こちらのURLは有効期限切れです"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_invitation.is_used = True
        user_invitation.save()
        user = user_invitation.user
        user.is_verified = True
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return JsonResponse(
            data={"msg": "新規ユーザの認証に成功しました"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def check_invitation_token(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(data={"check": False})

        check = self._check_invitation(serializer.data["token"]) != None
        return JsonResponse(data={"check": check})

    @action(detail=True, methods=["post"])
    def reinvite_user(self, request, pk):
        """ユーザを再招待する

        Args:
            request (HttpRequest): HttpRequestオブジェクト

        Returns:
            Union[
                HttpResponse,
                JsonResponse
            ]
        """
        try:
            user_invitation = UserInvitation.objects.select_related(
                "user"
            ).get(user_id=pk)
        except UserInvitation.DoesNotExist:
            return JsonResponse(
                data={"msg": "指定されたユーザは見つかりませんでした"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user_invitation.user.is_verified:
            return JsonResponse(
                data={"msg": "指定されたユーザは認証済です"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_invitation.token = secrets.token_urlsafe()
        user_invitation.expiry = timezone.now() + timedelta(days=1)
        user_invitation.save()
        base_url = django_settings.BASE_URL
        user = user_invitation.user
        url = base_url + "/verify-user/" + user_invitation.token
        send_invitation_email(
            email=user.email,
            url=url,
        )
        return JsonResponse(
            data={"msg": "招待メールを再送信しました"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["POST"])
    def send_reset_password_email(self, request):
        """指定したメールアドレス宛へパスワード再設定メールを送る

        Args:
            request: リクエスト

        Returns:
            HttpResponse
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(
                email=serializer.validated_data["email"],
            )
        except User.DoesNotExist as e:
            self.emergency_logger.error(e)
            return JsonResponse(
                data={},
            )
        if not user.is_active or not user.is_verified:
            self.application_logger.warning("ユーザは有効化済みまたは認証済みです")
            return JsonResponse(
                data={},
            )
        try:
            token = secrets.token_urlsafe(64)
            expiry = timezone.now() + timedelta(minutes=30)
            UserResetPassword.objects.create(
                token=token,
                user=user,
                expiry=expiry,
            )
        except DatabaseError as e:
            self.emergency_logger.error(e)
            return JsonResponse(
                data={},
            )
        base_url = django_settings.BASE_URL
        url = base_url + "/reset-password/" + token
        send_reset_email(
            email=user.email,
            url=url,
        )
        return JsonResponse(
            data={"msg": "パスワード再設定メールを送信しました"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def reset_password(self, request):
        """パスワード再設定用API

        Args:
            request: リクエスト

        Returns:
            JsonResponse
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_password = self.check_reset_password(serializer.data["token"])
        if reset_password is None:
            return JsonResponse(
                data={"msg": "有効期限切れのリンクです。管理者に再送信を依頼してください。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = reset_password.user
        user.set_password(serializer.data["password"])
        reset_password.is_used = True
        reset_password.save()
        user.save()
        return JsonResponse(data={"msg": "パスワードの再設定が完了しました"})

    @action(detail=False, methods=["post"])
    def check_reset_password_token(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(data={"check": False})

        check = self._check_reset_password(serializer.data["token"]) != None
        return JsonResponse(data={"check": check})

    @action(detail=True, methods=["post"])
    def toggle_user_active(self, request, pk):
        """ユーザを有効化/無効化するAPI
        Args:
            request : リクエスト
            pk : ユーザID
        Returns:
            JsonResponse
        """
        user = self.get_object()
        if request.user == user:
            return JsonResponse(
                data={"msg": "自身を無効化することはできません"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return JsonResponse(data={"is_active": user.is_active})

    @action(detail=False, methods=["get"])
    def user_info(self, request):
        """ユーザの情報を取得するAPI

        Args:
            request : リクエスト

        Returns:
            JsonResponse
        """
        data = {"name": None, "role": None}
        if request.user.is_authenticated:
            # パスワードが社員番号の場合is_initial_passwordはtrue
            data = {
                "name": request.user.username,
                "role": User.Role(request.user.role).label,
            }
        return JsonResponse(data=data)

    def _check_invitation(self, token):
        """ユーザ招待用トークンを確認する

        Args:
            token : ユーザ認証用トークン

        Returns:
            Union[
                UserInvitationオブジェクト,
                None
            ]
        """
        try:
            invitation = UserInvitation.objects.select_related("user").get(
                token=token,
                is_used=False,
            )
        except:
            return None

        if invitation.expiry < timezone.localtime() or invitation.is_used:
            return None
        return invitation

    def _check_reset_password(self, token):
        """パスワード再設定用トークンを確認する

        Args:
            token : パスワード再設定用トークン

        Returns:
            Union[
                UserResetPasswordオブジェクト,
                None
            ]
        """
        try:
            reset_password = UserResetPassword.objects.select_related(
                "user"
            ).get(
                token=token,
                is_used=False,
            )
        except:
            return None

        if reset_password.expiry < timezone.now() or reset_password.is_used:
            return None
        return reset_password
