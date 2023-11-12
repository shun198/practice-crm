# Generated by Django 4.2.5 on 2023-10-28 11:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTableComment(
            name="userinvitation",
            table_comment="ユーザ招待用",
        ),
        migrations.AlterModelTableComment(
            name="userresetpassword",
            table_comment="ユーザパスワード再設定",
        ),
        migrations.AlterField(
            model_name="userinvitation",
            name="token",
            field=models.CharField(
                db_comment="ユーザ招待用メールURL用トークン", max_length=255
            ),
        ),
        migrations.AlterField(
            model_name="userresetpassword",
            name="user",
            field=models.ForeignKey(
                db_comment="ユーザテーブル外部キー",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="user_password_reset",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelTable(
            name="userinvitation",
            table="Invitation",
        ),
        migrations.AlterModelTable(
            name="userresetpassword",
            table="PasswordReset",
        ),
    ]