from collections import OrderedDict

import pytest

from application.models import User
from application.serializers.user import UserSerializer
from application.utils.constants import Group


@pytest.mark.django_db
def test_user_serializer_to_representation(management_user):
    """to_representationで設定した形式で取得できる事を確認する"""

    serializer = UserSerializer(instance=management_user)
    expected = OrderedDict(
        [
            ("id", str(management_user.id)),
            ("employee_number", management_user.employee_number),
            ("username", management_user.username),
            ("email", management_user.email),
            ("group", management_user.group.name),
            ("is_active", management_user.is_active),
            ("is_verified", management_user.is_verified),
        ]
    )

    assert serializer.to_representation(serializer.instance) == expected


@pytest.fixture
def user_data():
    """システムユーザのインプットデータ"""

    return {
        "employee_number": "1" * 8,
        "username": "テストユーザ01",
        "email": "test@example.com",
        "group": Group.MANAGER.value,
    }


@pytest.mark.django_db
def test_validate_user_data(user_data):
    """userのデータがバリデーションエラーにならない"""
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_employee_number_length_cannot_be_7_or_shorter(user_data):
    """userのemployee_numberが7文字以下のためバリデーションエラーになる"""
    user_data["employee_number"] = "1" * 7
    serializer = UserSerializer(data=user_data)
    assert not serializer.is_valid()
