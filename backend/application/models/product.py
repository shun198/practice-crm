import uuid

from django.db import models


class Product(models.Model):
    """商品"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="商品ID",
    )
    name = models.CharField(
        max_length=255,
        db_comment="商品名",
    )
    details = models.TextField(
        blank=True,
        db_comment="商品の詳細",
    )
    price = models.PositiveIntegerField(default=0, db_comment="商品の金額")
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="作成日",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="更新日",
    )

    class Meta:
        db_table = "Product"
        db_table_comment = "商品"
