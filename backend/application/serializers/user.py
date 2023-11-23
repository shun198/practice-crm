from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from application.models import User


class UserSerializer(serializers.ModelSerializer):
    """ユーザ用シリアライザ"""

    class Meta:
        model = User
        fields = ["id", "employee_number", "username", "email", "role"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        rep["role"] = instance.get_role_display()
        return rep


class LoginSerializer(serializers.ModelSerializer):
    """ログイン用シリアライザ"""

    employee_number = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["employee_number", "password"]


class VerifyUserSerializer(serializers.Serializer):
    """ユーザ認証用シリアライザ"""

    token = serializers.CharField(max_length=255)
    """パスワード登録用メールURL用トークン"""
    new_password = serializers.CharField(max_length=255)
    """新規パスワード"""
    confirm_password = serializers.CharField(max_length=255)
    """新規パスワード再確認"""

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("新規パスワードと確認パスワードが違います")
        validate_password(data["new_password"])
        return data


class InviteUserSerializer(serializers.Serializer):
    """ユーザ招待用シリアライザ"""

    employee_number = serializers.CharField(min_length=8, max_length=8)
    """社員番号"""
    name = serializers.CharField(max_length=255)
    """社員指氏名"""
    email = serializers.EmailField(max_length=254)
    """社員メールアドレス"""


class ResetPasswordSerializer(serializers.Serializer):
    """パスワード再設定用シリアライザ"""

    token = serializers.CharField(max_length=255)
    """パスワード再設定メールURL用トークン"""
    new_password = serializers.CharField(max_length=255)
    """新規パスワード"""
    confirm_password = serializers.CharField(max_length=255)
    """新規パスワード再確認"""

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("新規パスワードと確認パスワードが違います")
        validate_password(data["new_password"])
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """パスワード変更用Serializer"""

    current_password = serializers.CharField(max_length=255)
    """現在のパスワード"""
    new_password = serializers.CharField(max_length=255)
    """新規パスワード"""
    confirm_password = serializers.CharField(max_length=255)
    """新規パスワード再確認"""

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("新規パスワードと確認パスワードが違います")
        validate_password(data["new_password"])
        return data


class CheckTokenSerializer(serializers.Serializer):
    """トークンが有効であるか確認するSerializer"""

    token = serializers.CharField(max_length=255)
    """トークン"""


class SendResetPasswordEmailSerializer(serializers.Serializer):
    """パスワード再設定メールを送信するSerializer"""

    email = serializers.EmailField(max_length=254)
    """社員メールアドレス"""
