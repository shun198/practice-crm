"""
権限用のモジュール
"""
from rest_framework.permissions import BasePermission


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
            if request.user.group.name == "管理者":
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
