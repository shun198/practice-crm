# Generated by Django 4.2.5 on 2023-11-18 11:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0002_alter_userinvitation_table_comment_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("prefecture", models.CharField(max_length=255)),
                ("municipalities", models.CharField(max_length=255)),
                ("house_no", models.CharField(max_length=255)),
                ("other", models.CharField(blank=True, max_length=255)),
                (
                    "post_no",
                    models.CharField(
                        max_length=7,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[0-9]{7}$", "7桁の数字を入力してください。"
                            )
                        ],
                    ),
                ),
            ],
            options={
                "db_table": "Address",
            },
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("kana", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("birthday", models.DateField()),
                (
                    "phone_no",
                    models.CharField(
                        blank=True,
                        max_length=11,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[0-9]{11}$", "11桁の数字を入力してください。"
                            )
                        ],
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address",
                        to="application.address",
                    ),
                ),
            ],
            options={
                "db_table": "Customer",
            },
        ),
    ]
