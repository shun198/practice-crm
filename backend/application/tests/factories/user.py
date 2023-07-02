from datetime import datetime, timedelta

from factory import Faker, PostGenerationMethodCall, Sequence
from factory.django import DjangoModelFactory

from application.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: "テスト利用者{}".format(n))
    employee_number = "11111111"
    password = PostGenerationMethodCall("set_password", "test")
    email = Faker("email")
    role = Faker(
        "random_int",
        min=0,
        max=2,
    )
    created_at = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=20)).date(),
        date_end=datetime.now(),
    )
    updated_at = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=20)).date(),
        date_end=datetime.now(),
    )
