# Generated by Django 4.2.4 on 2023-09-03 12:18

import uuid

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_comment="商品ID",
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(db_comment="商品名", max_length=255)),
                ("details", models.TextField(blank=True, db_comment="商品の詳細")),
                (
                    "price",
                    models.PositiveIntegerField(db_comment="商品の金額", default=0),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, db_comment="作成日"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, db_comment="更新日"),
                ),
            ],
            options={
                "db_table": "Product",
                "db_table_comment": "商品",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        db_comment="システムユーザID",
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "employee_number",
                    models.CharField(
                        db_comment="社員番号",
                        max_length=8,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator("^[0-9]{8}$")
                        ],
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        db_comment="ユーザ名",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        db_comment="メールアドレス", max_length=254, unique=True
                    ),
                ),
                (
                    "role",
                    models.PositiveIntegerField(
                        choices=[
                            (0, "Management"),
                            (1, "General"),
                            (2, "Part Time"),
                        ],
                        db_comment="システムユーザのロール",
                        default=2,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, db_comment="作成日"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, db_comment="更新日"),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "db_table": "User",
                "db_table_comment": "システムユーザ",
                "ordering": ["employee_number"],
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
