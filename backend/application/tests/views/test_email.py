import pytest
from application.tests.common_method import login, mail_confirm
from django.core import mail
from rest_framework import status


@pytest.fixture
def send_invite_user_mail_url():
    return "/api/users/send_invite_user_mail/"

@pytest.mark.django_db()
def test_management_user_can_send_invite_user_email(
    client, login_management, send_invite_user_mail_url, email_data
):
    """管理者ユーザで正常に招待メールを送信できることをテスト"""
    login(client, login_management)
    response = client.post(send_invite_user_mail_url, email_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    mail_confirm(mail.outbox, email_data["email"], "ようこそ")

@pytest.mark.django_db()
def test_general_user_cannot_send_invite_user_email(
    client, login_general, send_invite_user_mail_url, email_data
):
    """一般ユーザで正常に招待メールを送信できないことをテスト"""
    login(client, login_general)
    response = client.post(send_invite_user_mail_url, email_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db()
def test_part_time_user_cannot_send_invite_user_email(
    client, login_part_time, send_invite_user_mail_url, email_data
):
    """アルバイトユーザで招待メールを送信できないことをテスト"""
    login(client, login_part_time)
    response = client.post(send_invite_user_mail_url, email_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN