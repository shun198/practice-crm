from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from application.emails import send_welcome_email
from application.models.user import User
from application.permissions import (
    IsGeneralUser,
    IsManagementUser,
    IsPartTimeUser,
    IsSuperUser,
)
from application.serializers.user import EmailSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "send_invite_user_mail":
            return EmailSerializer
        else:
            return UserSerializer

    @action(detail=False, methods=["POST"])
    def send_invite_user_mail(self, request):
        """指定したメールアドレス宛へ招待メールを送る

        Args:
            request: リクエスト

        Returns:
            HttpResponse
        """
        serializer = self.get_serializer(data=request.data)
        # バリデーションに失敗したら400を返す
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        email = serializer.validated_data.get("email")
        # メール送信用メソッド
        send_welcome_email(email=email)
        return HttpResponse()

    # get_permissionsメソッドを使えば前述の表に従って権限を付与できる
    def get_permissions(self):
        if self.action in [
            "update",
            "partial_update",
            "send_invite_user_mail",
        ]:
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
