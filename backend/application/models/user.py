import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """システムユーザ"""

    username_validator = UnicodeUsernameValidator()

    class Role(models.IntegerChoices):
        """システムユーザのロール

        Args:
            MANAGEMENT(0): 管理者
            GENERAL(1):    一般
        """

        MANAGEMENT = 0, "管理者"
        GENERAL = 1, "一般"

    # 不要なフィールドはNoneにすることができる
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="システムユーザID",
    )
    employee_number = models.CharField(
        unique=True,
        validators=[RegexValidator(r"^[0-9]{8}$")],
        max_length=8,
        db_comment="社員番号",
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        db_comment="ユーザ名",
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        db_comment="メールアドレス",
    )
    role = models.PositiveIntegerField(
        choices=Role.choices,
        default=Role.MANAGEMENT,
        db_comment="システムユーザのロール",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="作成日",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="更新日",
    )
    is_verified = models.BooleanField(
        default=False,
        db_comment="有効化有無",
    )
    created_by = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        db_comment="作成者",
    )
    updated_by = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        db_comment="更新者",
    )

    USERNAME_FIELD = "employee_number"
    REQUIRED_FIELDS = ["email", "username"]

    class Meta:
        ordering = ["employee_number"]
        db_table = "User"
        db_table_comment = "システムユーザ"

    def save(self, *args, **kwargs):
        # 既に登録されているシステム利用者情報の保存処理
        if self.id:
            if not "updated_by" in kwargs:
                self.updated_by = self
            else:
                self.updated_by = kwargs.get("updated_by")
                kwargs.pop("updated_by")
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class UserResetPassword(models.Model):
    """ユーザパスワード再設定テーブルに対応するモデルクラス"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="システムユーザID",
    )
    token = models.CharField(
        max_length=255,
        db_comment="パスワード設定メールURL用トークン",
    )
    expiry = models.DateTimeField(
        null=True,
        default=None,
        db_comment="有効期限",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="作成日時",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="user_password_reset",
        db_comment="ユーザテーブル外部キー",
    )
    is_used = models.BooleanField(
        default=False,
        db_comment="使用有無",
    )

    class Meta:
        db_table = "PasswordReset"
        db_table_comment = "ユーザパスワード再設定"


class UserInvitation(models.Model):
    """ユーザ招待用テーブルに対応するモデルクラス"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="システムユーザID",
    )
    token = models.CharField(
        max_length=255,
        db_comment="ユーザ招待用メールURL用トークン",
    )
    expiry = models.DateTimeField(
        null=True,
        default=None,
        db_comment="有効期限",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="作成日時",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="user_invitation",
        db_comment="社員テーブル外部キー",
    )
    is_used = models.BooleanField(
        default=False,
        db_comment="使用有無",
    )

    class Meta:
        db_table = "Invitation"
        db_table_comment = "ユーザ招待用"
