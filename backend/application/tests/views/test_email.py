import pytest
from django.core import mail
from rest_framework import status

from application.tests.common_method import login, mail_confirm


@pytest.fixture
def send_invite_user_mail_url():
    return "/api/users/invite_user/"

@pytest.fixture
def email_data():
    return {
        "employee_number": "00000010",
        "email": "test_user_01@test.com",
        "name": "test_user_01",
    }


@pytest.mark.django_db()
def test_management_user_can_send_invite_user_email(
    client, login_management, send_invite_user_mail_url, email_data
):
    """管理者ユーザで正常に招待メールを送信できることをテスト"""
    login(client, login_management)
    response = client.post(
        send_invite_user_mail_url, email_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    mail_confirm(mail.outbox, email_data["email"], "アカウント登録のお知らせ")


@pytest.mark.django_db()
def test_general_user_cannot_send_invite_user_email(
    client, login_general, send_invite_user_mail_url, email_data
):
    """一般ユーザで正常に招待メールを送信できないことをテスト"""
    login(client, login_general)
    response = client.post(
        send_invite_user_mail_url, email_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
def test_part_time_user_cannot_send_invite_user_email(
    client, login_part_time, send_invite_user_mail_url, email_data
):
    """アルバイトユーザで招待メールを送信できないことをテスト"""
    login(client, login_part_time)
    response = client.post(
        send_invite_user_mail_url, email_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
