from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from application.models import User


class UserSerializer(serializers.ModelSerializer):
    """ユーザ用シリアライザ"""

    class Meta:
        model = User
        fields = [
            "id",
            "employee_number",
            "username",
            "email",
            "group",
            "is_active",
            "is_verified",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "is_active",
            "is_verified",
        ]

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        rep["group"] = instance.group.name
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


class InviteUserSerializer(serializers.ModelSerializer):
    """ユーザ招待用シリアライザ"""

    def create(self, validated_data, created_by, updated_by):
        return User.objects.create_user(
            created_by=created_by, updated_by=updated_by, **validated_data
        )

    class Meta:
        model = User
        fields = [
            "employee_number",
            "username",
            "group",
            "email",
        ]

    def validate_group(self, value):
        try:
            data = Group.objects.get(name=value)
        except Group.DoesNotExist:
            raise serializers.ValidationError("指定された権限は存在しません。")
        return data


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
