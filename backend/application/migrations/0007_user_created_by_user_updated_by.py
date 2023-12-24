# Generated by Django 4.2.8 on 2023-12-24 03:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0006_photo_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="created_by",
            field=models.ForeignKey(
                db_comment="作成者",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="updated_by",
            field=models.ForeignKey(
                db_comment="更新者",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]