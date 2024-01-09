from datetime import timedelta

import pytest
from django.utils import timezone
from freezegun import freeze_time

from application.filters import CustomerFilter, UserFilter
from application.models import User
from application.tests.factories.customer import (
    AddressFactory,
    CustomerFactory,
)
from application.tests.factories.user import UserFactory


@pytest.mark.django_db
def test_user_filter_email_contains():
    """システムユーザ名を部分一致でフィルターできる事を確認する"""

    user = UserFactory(username="テストフィルターユーザ")
    user_filter = UserFilter({"email__contains": "テストフィルター"})
    assert user_filter.qs.count() == 1
    assert user_filter.qs[0] == user


@pytest.mark.django_db
def test_user_filter_email_contains():
    """メールアドレスを部分一致でフィルターできる事を確認する"""

    user = UserFactory(email="test_filter@test.com")
    user_filter = UserFilter({"email__contains": "test_filter"})
    assert user_filter.qs.count() == 1
    assert user_filter.qs[0] == user


@pytest.mark.django_db
def test_inquiry_application_date_range_filter():
    """作成日をフィルターできることを確認する"""

    today = timezone.now()
    with freeze_time(today):
        first_user = UserFactory()
        second_user = UserFactory()
        inquiry_filter = UserFilter({"created_at_after": today})
        assert inquiry_filter.qs.count() == 2
        assert inquiry_filter.qs[0] == first_user
        assert inquiry_filter.qs[1] == second_user


@pytest.mark.django_db
def test_customer_name_kana_filter_contains():
    """氏名・カナ氏名でフィルターできる事を確認する"""

    customer = CustomerFactory(
        name="降田絞込",
        kana="フィルタシボリコミ",
    )
    customer_filter = CustomerFilter({"name": "降田絞込"})
    assert customer_filter.qs.count() == 1
    assert customer_filter.qs[0] == customer
    customer_filter = CustomerFilter({"name": "フィルタシボリコミ"})
    assert customer_filter.qs.count() == 1
    assert customer_filter.qs[0] == customer


@pytest.mark.django_db
def test_customer_address_filter_contains():
    """住所でフィルターできる事を確認する"""

    address = AddressFactory()
    customer = CustomerFactory(address=address)
    customer_filter = CustomerFilter({"address": f"{address.prefecture}"})
    assert customer_filter.qs.count() == 1
    assert customer_filter.qs[0] == customer
    customer_filter = CustomerFilter({"address": f"{address.municipalities}"})
    assert customer_filter.qs.count() == 1
    assert customer_filter.qs[0] == customer
    customer_filter = CustomerFilter({"address": f"{address.house_no}"})
    assert customer_filter.qs.count() == 1
    assert customer_filter.qs[0] == customer
    customer_filter = CustomerFilter({"address": f"{address.other}"})
    assert customer_filter.qs.count() == 1
    assert customer_filter.qs[0] == customer


@pytest.mark.django_db
def test_customer_birthday_filter_exact():
    """誕生日を完全一致でフィルターできる事を確認する"""

    customer = CustomerFactory(birthday="1955-01-01")
    customer_filter = CustomerFilter({"birthday": "1955-01-01"})
    assert customer_filter.qs.count() == 1
    assert customer_filter.qs[0] == customer


@pytest.mark.django_db
def test_customer_filter_email_contains():
    """メールアドレスを部分一致でフィルターできる事を確認する"""

    customer = CustomerFactory(email="test_filter@test.com")
    customer_filter = CustomerFilter({"email__contains": "test_filter"})
    assert customer_filter.qs.count() == 1
    assert customer_filter.qs[0] == customer


@pytest.mark.django_db
def test_customer_phone_no_filter_starts_with():
    """電話番号を前からフィルターできる事を確認する"""

    customer = CustomerFactory(phone_no="0120201810")
    customer_filter = CustomerFilter({"phone_no__startswith": "01202018"})
    assert customer_filter.qs.count() == 1
    assert customer_filter.qs[0] == customer
