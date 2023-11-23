# Generated by Django 4.2.7 on 2023-11-23 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0002_alter_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="userinvitation",
            name="is_used",
            field=models.BooleanField(db_comment="使用有無", default=False),
        ),
        migrations.AddField(
            model_name="userresetpassword",
            name="is_used",
            field=models.BooleanField(db_comment="使用有無", default=False),
        ),
    ]
