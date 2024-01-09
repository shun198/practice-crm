from django.contrib.auth.models import BaseUserManager, Group


class UserManager(BaseUserManager):
    """システム利用者を作成する為のクラス"""

    use_in_migrations = True

    def create_user(
        self,
        name: str,
        employee_number: str,
        **extra_fields,
    ):
        """システム利用者を作成

        Args:
            name (str): システム利用者名
            employee_number (str): 社員番号
            group (UserGroup): システム利用者権限
        Returns:
            作成したシステム利用者
        """

        group, _ = Group.objects.get_or_create(name=group.value)

        user = self.model(
            name=name,
            employee_number=employee_number,
            groups=group,
            **extra_fields,
        )
        # 初期バスワードは社員番号
        user.set_password(employee_number)
        user.save(using=self._db)

        return user
