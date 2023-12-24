from datetime import datetime, timedelta

import factory
from factory.django import DjangoModelFactory

from application.models import Address, Customer
from application.tests.factories.user import UserFactory


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    prefecture = factory.Faker("administrative_unit", locale="ja_JP")
    municipalities = factory.Faker("city", locale="ja_JP")
    house_no = str(factory.Faker("ban", locale="ja_JP")) + str(
        factory.Faker("gou", locale="ja_JP")
    )
    other = str(factory.Faker("building_name", locale="ja_JP")) + str(
        factory.Faker("building_number", locale="ja_JP")
    )
    post_no = factory.Faker("random_number", digits=7)


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    kana = factory.Sequence(lambda n: "テストコキャク{}".format(n))
    name = factory.Sequence(lambda n: "テスト顧客{}".format(n))
    birthday = factory.Faker(
        "date_between_dates",
        date_start=(datetime.now().date() - timedelta(days=365 * 50)),
        date_end=(datetime.now().date() - timedelta(days=365 * 20)),
    )
    email = factory.Faker("email")
    phone_no = factory.Sequence(lambda n: f"080" + "{0:08}".format(n + 100))
    address = factory.SubFactory(AddressFactory)
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)
