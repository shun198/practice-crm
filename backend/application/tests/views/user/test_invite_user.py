import pytest
from django.core import mail
from rest_framework import status

from application.models import User, UserInvitation
from application.tests.common_method import mail_confirm
from application.utils.constants import Group


@pytest.fixture
def get_invite_user_url():
    """社員招待用のurl"""
    return "/api/users/invite_user"


@pytest.fixture
def post_invite_user_data():
    """社員招待用のインプットデータ"""
    return {
        "employee_number": "99999990",
        "username": "テストユーザ01",
        "group": Group.MANAGER.value,
        "email": "test_user@test.com",
    }


@pytest.mark.django_db
def test_invite_user_management(
    client,
    management_user,
    password,
    get_invite_user_url,
    post_invite_user_data,
):
    """管理者がシステムユーザを招待できることを確認"""

    client.login(
        employee_number=management_user.employee_number, password=password
    )
    response = client.post(
        get_invite_user_url,
        post_invite_user_data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "招待メールを送信しました"}
    mail_confirm(
        mail.outbox,
        sender=post_invite_user_data["email"],
        message="アカウント登録のお知らせ",
    )
    user = User.objects.get(
        employee_number=post_invite_user_data["employee_number"]
    )
    assert user
    assert UserInvitation.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_cannot_invite_user_general(
    client,
    general_user,
    password,
    get_invite_user_url,
    post_invite_user_data,
):
    """一般ユーザがシステムユーザを招待できないことを確認"""

    client.login(
        employee_number=general_user.employee_number,
        password=password,
    )
    response = client.post(
        get_invite_user_url,
        post_invite_user_data,
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert len(mail.outbox) == 0
