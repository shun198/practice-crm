import uuid

from django.core.validators import RegexValidator
from django.db import models


class Customer(models.Model):
    """お客様"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="ID",
    )
    kana = models.CharField(
        max_length=255,
        db_comment="カナ氏名",
    )
    name = models.CharField(
        max_length=255,
        db_comment="氏名",
    )
    birthday = models.DateField(
        db_comment="誕生日",
    )
    email = models.EmailField(
        db_comment="メールアドレス",
    )
    phone_no = models.CharField(
        max_length=11,
        validators=[RegexValidator(r"^[0-9]{11}$", "11桁の数字を入力してください。")],
        blank=True,
        db_comment="電話番号",
    )
    address = models.OneToOneField(
        "Address",
        on_delete=models.CASCADE,
        related_name="address",
        db_comment="住所のFK",
    )

    class Meta:
        db_table = "Customer"


class Address(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="ID",
    )
    prefecture = models.CharField(
        max_length=255,
        db_comment="都道府県",
    )
    municipalities = models.CharField(
        max_length=255,
        db_comment="市区町村",
    )
    house_no = models.CharField(
        max_length=255,
        db_comment="丁・番地",
    )
    other = models.CharField(
        max_length=255,
        blank=True,
        db_comment="その他(マンション名など)",
    )
    post_no = models.CharField(
        max_length=7,
        validators=[RegexValidator(r"^[0-9]{7}$", "7桁の数字を入力してください。")],
        null=True,
        db_comment="郵便番号",
    )

    class Meta:
        db_table = "Address"
