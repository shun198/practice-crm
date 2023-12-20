from datetime import datetime, timedelta

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError

from application.models import Address, Customer
from application.tests.factories.customer import (
    AddressFactory,
    CustomerFactory,
)


def get_customer(id):
    return Customer.objects.get(pk=id)


def get_address(id):
    return Address.objects.get(pk=id)


@pytest.mark.django_db
def test_kana_length_can_be_255():
    """カナ氏名の長さの最大値が255文字"""
    kana = "a" * 255
    customer = CustomerFactory(kana=kana)
    assert get_customer(customer.id).kana == kana


@pytest.mark.django_db
def test_name_length_can_be_255():
    """カナ氏名の長さの最大値が255文字"""
    name = "a" * 255
    customer = CustomerFactory(name=name)
    assert get_customer(customer.id).name == name


@pytest.mark.django_db
def test_birthday_can_be_date():
    """誕生日が日付のフォーマット"""
    birthday = datetime.now().date() - timedelta(days=365 * 20)
    customer = CustomerFactory(birthday=birthday)
    assert get_customer(customer.id).birthday == birthday


@pytest.mark.django_db
def test_birthday_is_not_date():
    """誕生日が日付以外のフォーマット"""
    birthday = "1995-09-1-8"
    with pytest.raises(ValidationError):
        CustomerFactory(birthday=birthday)


@pytest.mark.django_db
def test_birthday_cannot_be_null():
    """誕生日nullにできない"""
    with pytest.raises(IntegrityError):
        CustomerFactory(birthday=None)


@pytest.mark.django_db
def test_phone_length_can_be_11():
    """phone_numberの長さの最大値が11文字"""
    phone_no = "080" + "1" * 8
    customer = CustomerFactory(phone_no=phone_no)
    assert get_customer(customer.id).phone_no == phone_no


@pytest.mark.django_db
def test_phone_length_cannot_be_12_or_longer():
    """phone_numberの長さが12文字以上にならない"""
    phone_no = "080" + "1" * 9
    with pytest.raises(DataError):
        CustomerFactory(phone_no=phone_no)


@pytest.mark.django_db
def test_phone_length_cannot_be_null():
    """phone_numberはnullにならない"""
    with pytest.raises(IntegrityError):
        CustomerFactory(phone_no=None)


@pytest.mark.django_db
def test_prefecture_length_can_be_255():
    """都道府県の長さの最大値が255文字"""
    prefecture = "a" * 255
    address = AddressFactory(prefecture=prefecture)
    assert get_address(address.id).prefecture == prefecture


@pytest.mark.django_db
def test_municipalities_length_can_be_255():
    """市区町村の長さの最大値が255文字"""
    municipalities = "a" * 255
    address = AddressFactory(municipalities=municipalities)
    assert get_address(address.id).municipalities == municipalities


@pytest.mark.django_db
def test_house_no_length_can_be_255():
    """丁・番地の長さの最大値が255文字"""
    house_no = "a" * 255
    address = AddressFactory(house_no=house_no)
    assert get_address(address.id).house_no == house_no


@pytest.mark.django_db
def test_other_length_can_be_255():
    """その他の長さの最大値が255文字"""
    other = "a" * 255
    address = AddressFactory(other=other)
    assert get_address(address.id).other == other


@pytest.mark.django_db
def test_post_no_length_can_be_7():
    """郵便番号の長さの最大値が7文字"""
    post_no = "1" * 7
    address = AddressFactory(post_no=post_no)
    assert get_address(address.id).post_no == post_no


@pytest.mark.django_db
def test_post_no_length_can_be_8_or_longer():
    """郵便番号の長さが8文字以上にならない"""
    post_no = "1" * 8
    with pytest.raises(DataError):
        AddressFactory(post_no=post_no)
