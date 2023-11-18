import uuid

from django.core.validators import RegexValidator
from django.db import models


class Customer(models.Model):
    """お客様"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kana = models.CharField(max_length=255)
    """カナ氏名"""
    name = models.CharField(max_length=255)
    """氏名"""
    birthday = models.DateField()
    """誕生日"""
    phone_no = models.CharField(
        max_length=11,
        validators=[RegexValidator(r"^[0-9]{11}$", "11桁の数字を入力してください。")],
        blank=True,
    )
    """電話番号"""
    address = models.ForeignKey(
        "Address",
        on_delete=models.CASCADE,
        related_name="address",
    )
    """住所"""

    class Meta:
        db_table = "Customer"


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prefecture = models.CharField(max_length=255)
    """都道府県"""
    municipalities = models.CharField(max_length=255)
    """市区町村"""
    house_no = models.CharField(max_length=255)
    """丁・番地"""
    other = models.CharField(max_length=255, blank=True)
    """その他(マンション名など)"""
    post_no = models.CharField(
        max_length=7,
        validators=[RegexValidator(r"^[0-9]{7}$", "7桁の数字を入力してください。")],
        null=True,
    )
    """郵便番号"""

    class Meta:
        db_table = "Address"
