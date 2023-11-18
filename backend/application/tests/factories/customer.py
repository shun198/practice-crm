from datetime import datetime, timedelta

import factory
from factory import Faker, Sequence, SubFactory

from application.models import Address, Customer


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    prefecture = Faker("administrative_unit", locale="ja_JP")
    municipalities = Faker("city", locale="ja_JP")
    house_no = str(Faker("ban", locale="ja_JP")) + str(
        Faker("gou", locale="ja_JP")
    )
    other = str(Faker("building_name", locale="ja_JP")) + str(
        Faker("building_number", locale="ja_JP")
    )
    post_no = Faker("random_number", digits=7)


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    kana = Sequence(lambda n: "テストコキャク{}".format(n))
    name = Sequence(lambda n: "テスト顧客{}".format(n))
    birthday = Faker(
        "date_between_dates",
        date_start=(datetime.now().date() - timedelta(days=365 * 50)),
        date_end=(datetime.now().date() - timedelta(days=365 * 20)),
    )
    phone_no = Sequence(lambda n: f"080" + "{0:08}".format(n + 100))
    address = SubFactory(AddressFactory)
