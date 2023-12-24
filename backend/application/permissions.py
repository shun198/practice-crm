"""
権限用のモジュール
"""
from rest_framework.permissions import BasePermission

from application.models import User


class IsGeneralUser(BasePermission):
    def has_permission(self, request, view):
        """一般ユーザかどうか判定

        Args:
            request: リクエスト
            view: ビュー
        Returns:
            一般ユーザならTrue
            それ以外はFalse
        """
        if request.user.is_superuser:
            return True

        if request.user.is_authenticated:
            # 一般ユーザー、管理ユーザーともにTrueになるよう設定
            if request.user.role in [
                User.Role.GENERAL,
                User.Role.MANAGEMENT,
            ]:
                return True
        return False


class IsManagementUser(BasePermission):
    def has_permission(self, request, view):
        """管理ユーザかどうか判定

        Args:
            request: リクエスト
            view: ビュー

        Returns:
            管理ユーザならTrue
            それ以外はFalse
        """
        if request.user.is_superuser:
            return True

        if request.user.is_authenticated:
            if request.user.role == User.Role.MANAGEMENT:
                return True
        return False


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        """スーパーユーザかどうか判定

        Args:
            request: リクエスト
            view: ビュー

        Returns:
            スーパーユーザならTrue
            それ以外はFalse
        """
        return request.user.is_superuser
