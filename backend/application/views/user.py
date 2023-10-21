from application.emails import send_welcome_email
from application.models.user import User, UserResetPassword
from application.permissions import (
    IsGeneralUser,
    IsManagementUser,
    IsPartTimeUser,
    IsSuperUser,
)
from application.serializers.user import (
    CreatePasswordSerializer,
    EmailSerializer,
    InviteUserSerializer,
    UserSerializer,
)
from application.utils.csv_wrapper import CSVResponseWrapper, CSVUserListData
from django.contrib.auth import update_session_auth_hash
from django.db import DatabaseError, transaction
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from project.settings.environment import django_settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        match self.action:
            case "send_invite_user_mail":
                return EmailSerializer
            case "change_password":
                return CreatePasswordSerializer
            case "invite_user":
                return InviteUserSerializer
            case _:
                return UserSerializer

    @action(detail=False, methods=["POST"])
    def invite_user(self, request):
        """指定したメールアドレス宛へ招待メールを送る

        Args:
            request: リクエスト

        Returns:
            HttpResponse
        """
        serializer = self.get_serializer(data=request.data)
        # バリデーションに失敗したら400を返す
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get("name")
        email = serializer.validated_data.get("email")
        if User.objects.filter(email=email).exists():
            return JsonResponse(data={"msg":"すでに有効化済みのユーザです"})
        base_url = django_settings.BASE_URL
        # 初回登録用のURLへ遷移
        url = base_url + "/verify-user/"
        # メール送信用メソッド
        send_welcome_email(email=email, name=name, url=url)
        return Response()

    # get_permissionsメソッドを使えば前述の表に従って権限を付与できる
    def get_permissions(self):
        if self.action in {
            "update",
            "partial_update",
            "send_invite_user_mail",
        }:
            permission_classes = [IsManagementUser]
        elif self.action == "create":
            permission_classes = [IsGeneralUser]
        elif self.action == "destroy":
            permission_classes = [IsSuperUser]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsPartTimeUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=["post"], detail=False)
    def export(self, request):
        """
        CSV形式でユーザー一覧をエクスポートするAPI
        Returns:
            CSVファイル
        """
        csvWrapper = CSVResponseWrapper("user_data.csv")
        csv_data = CSVUserListData(self.queryset)
        csvWrapper.write_response(csv_data)

        return csvWrapper.response

    @action(methods=["post"], detail=False)
    def change_password(self, request):
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
        update_session_auth_hash(request, user)
        return HttpResponse()


    @action(detail=False, methods=["post"])
    def create_password(self, request):
        """パスワード登録をする

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

        try:
            user_reset_password = UserResetPassword.objects.get(
                token=serializer.validated_data["token"]
            )
        except UserResetPassword.DoesNotExist:
            return JsonResponse(
                data={"msg": "無効なURLです"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if (
            user_reset_password.expiry is not None
            and user_reset_password.expiry < timezone.now()
        ):
            return JsonResponse(
                data={"msg": "こちらのURLは有効期限切れです"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            with transaction.atomic():
                user = user_reset_password.user
                user.is_invitation_completed = True
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                user_reset_password.delete()
        except DatabaseError:
            return JsonResponse(
                data={"msg": "パスワードの登録に失敗しました"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return HttpResponse()


    @action(detail=False, methods=["post"])
    def invite_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pass
        except BaseException:
            return JsonResponse(
                data={"msg": "ユーザの招待に失敗しました"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return HttpResponse()
            
            
    @action(detail=False, methods=["post"])
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pass
        except BaseException:
            return JsonResponse(
                data={"msg": "ユーザの招待に失敗しました"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return HttpResponse()