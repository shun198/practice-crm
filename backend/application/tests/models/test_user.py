import pytest
from django.db.utils import DataError, IntegrityError

from application.models import User
from application.tests.factories.user import UserFactory


def get_user(id):
    return User.objects.get(pk=id)


@pytest.mark.django_db
def test_employee_number_length_can_be_8():
    """employee_numberの長さの最大値が8文字"""
    employee_number = "1" * 8
    user = UserFactory(employee_number=employee_number)
    assert get_user(user.id).employee_number == employee_number


@pytest.mark.django_db
def test_employee_number_length_cannot_be_9_or_longer():
    """employee_numberの長さが9文字以上にならない"""
    employee_number = "1" * 9
    with pytest.raises(DataError):
        UserFactory(employee_number=employee_number)


@pytest.mark.django_db
def test_employee_number_length_cannot_be_null():
    """employee_numberはnullにならない"""
    with pytest.raises(IntegrityError):
        UserFactory(employee_number=None)


@pytest.mark.django_db
def test_employee_number_must_be_unique():
    """employee_numberはuniqueでなければならない"""
    employee_number = "1" * 8
    UserFactory(employee_number=employee_number)
    with pytest.raises(IntegrityError):
        UserFactory(employee_number=employee_number)


@pytest.mark.django_db
def test_username_length_can_be_150():
    """usernameの長さの最大値が150文字"""
    username = "a" * 150
    user = UserFactory(username=username)
    assert get_user(user.id).username == username


@pytest.mark.django_db
def test_username_length_cannot_be_151_or_longer():
    """usernameの長さの最大値が151文字以上にならない"""
    username = "a" * 151
    with pytest.raises(DataError):
        UserFactory(username=username)


@pytest.mark.django_db
def test_username_cannot_be_null():
    """usernameはnullにできない"""
    with pytest.raises(IntegrityError):
        UserFactory(username=None)


@pytest.mark.django_db
def test_username_must_be_unique():
    """usernameはuniqueでなければならない"""
    username = "a" * 150
    UserFactory(username=username)
    with pytest.raises(IntegrityError):
        UserFactory(username=username)


@pytest.mark.django_db
def test_email_length_can_be_254():
    """emailの長さの最大値が254文字"""
    email = "a" * 245 + "@test.com"
    user = UserFactory(email=email)
    assert get_user(user.id).email == email


@pytest.mark.django_db
def test_email_length_cannot_be_255_or_longer():
    """emailの長さの最大値が255文字以上にならない"""
    email = "a" * 246 + "@test.com"
    with pytest.raises(DataError):
        UserFactory(email=email)


@pytest.mark.django_db
def test_email_cannot_be_null():
    """emailはnullにできない"""
    with pytest.raises(IntegrityError):
        UserFactory(email=None)


@pytest.mark.django_db
def test_email_must_be_unique():
    """emailはuniqueでなければならない"""
    email = "a" * 245 + "@test.com"
    UserFactory(email=email)
    with pytest.raises(IntegrityError):
        UserFactory(email=email)
