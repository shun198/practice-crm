from datetime import timedelta

import pytest
from django.core import mail
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status

from application.models import User, UserResetPassword
from application.tests.common_method import mail_confirm
from application.tests.factories.user import UserFactory
from application.tests.factories.user_reset_password import (
    UserResetPasswordFactory,
)


@pytest.fixture
def get_send_reset_password_mail_url():
    """パスワード再設定メール送信用のurl"""
    return "/api/users/send_reset_password_email"


@pytest.fixture
def post_send_reset_password_mail_data(management_user):
    """パスワード再設定メール送信用のインプットデータ"""
    return {
        "email": management_user.email,
    }


@pytest.mark.django_db
def test_send_reset_password_email(
    client,
    management_user,
    get_send_reset_password_mail_url,
    post_send_reset_password_mail_data,
):
    """パスワード再設定メールを送信できることを確認"""

    response = client.post(
        get_send_reset_password_mail_url,
        post_send_reset_password_mail_data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    mail_confirm(
        mail.outbox,
        sender=management_user.email,
        message="パスワード再設定のお知らせ",
    )
    assert UserResetPassword.objects.filter(user=management_user).exists()


@pytest.mark.django_db
def test_send_reset_password_mail_user_does_not_exist(
    client,
    get_send_reset_password_mail_url,
    post_send_reset_password_mail_data,
):
    """ユーザが存在しない時はパスワード再設定メールを送信できないことを確認"""

    # 存在しない社員番号に変更
    post_send_reset_password_mail_data["email"] = "non_existing_user@email.com"
    response = client.post(
        get_send_reset_password_mail_url,
        post_send_reset_password_mail_data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_send_reset_password_mail_user_is_not_active(
    client,
    get_send_reset_password_mail_url,
    post_send_reset_password_mail_data,
):
    """ユーザが無効化されている時はパスワード再設定メールを送信できないことを確認"""

    user = UserFactory(is_active=False)
    post_send_reset_password_mail_data["email"] = user.email
    response = client.post(
        get_send_reset_password_mail_url,
        post_send_reset_password_mail_data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_send_reset_password_mail_user_is_not_verified(
    client,
    get_send_reset_password_mail_url,
    post_send_reset_password_mail_data,
):
    """ユーザの認証が完了されている時はパスワード再設定メールを送信できないことを確認"""

    user = UserFactory(is_verified=False)
    post_send_reset_password_mail_data["email"] = user.email
    response = client.post(
        get_send_reset_password_mail_url,
        post_send_reset_password_mail_data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.fixture
def get_reset_password_url():
    """パスワード再設定用のurl"""
    return "/api/users/reset_password"


@pytest.mark.django_db
def test_reset_password(
    client,
    get_reset_password_url,
):
    """パスワード再設定できることを確認"""
    user = UserFactory()
    reset_password = UserResetPasswordFactory(user=user)
    post_reset_password = {
        "token": reset_password.token,
        "new_password": "Test@123",
        "confirm_password": "Test@123",
    }

    response = client.post(
        get_reset_password_url,
        post_reset_password,
        format="json",
    )
    user = User.objects.get(id=user.id)
    reset_password = UserResetPassword.objects.get(user_id=user.id)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "パスワードの再設定が完了しました"}
    assert reset_password.user
    assert reset_password.is_used
    assert user.check_password(post_reset_password["new_password"])


@pytest.mark.django_db
def test_reset_password_token_is_invalid(
    client,
    get_reset_password_url,
):
    """パスワード再設定用トークンの有効期限が切れているため、パスワードを再設定できないことを確認"""
    user = UserFactory()
    reset_password = UserResetPasswordFactory(user=user)
    post_reset_password = {
        "token": reset_password.token,
        "new_password": "Test@123",
        "confirm_password": "Test@123",
    }
    expiry_time = timezone.localtime() + timedelta(minutes=31)
    with freeze_time(expiry_time):
        response = client.post(
            get_reset_password_url,
            post_reset_password,
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"msg": "有効期限切れのリンクです。管理者に再送信を依頼してください"}
