from datetime import timedelta

import pytest
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status

from application.models import User, UserInvitation
from application.tests.factories.user import UserFactory
from application.tests.factories.user_invitation import UserInvitationFactory


@pytest.fixture
def get_verify_user_url():
    """社員登録用のurl"""
    return "/api/users/verify_user"


@pytest.mark.django_db
def test_verify_user_management(
    client,
    management_user,
    password,
    get_verify_user_url,
):
    """管理者がシステムユーザを作成(認証)できることを確認"""
    client.login(
        employee_number=management_user.employee_number,
        password=password,
    )
    user = UserFactory(is_verified=False)
    invitation = UserInvitationFactory(
        user=user,
    )
    post_invite_user_data = {
        "token": invitation.token,
        "new_password": "Test@123",
        "confirm_password": "Test@123",
    }
    response = client.post(
        get_verify_user_url,
        post_invite_user_data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "新規ユーザの認証に成功しました"}
    assert User.objects.get(id=user.id).is_verified
    assert UserInvitation.objects.get(id=invitation.id).is_used


@pytest.mark.django_db
def test_verify_user_general(
    client,
    general_user,
    password,
    get_verify_user_url,
):
    """一般ユーザがシステムユーザを作成(認証)できることを確認"""
    client.login(
        employee_number=general_user.employee_number,
        password=password,
    )
    user = UserFactory(is_verified=False)
    invitation = UserInvitationFactory(
        user=user,
    )
    post_invite_user_data = {
        "token": invitation.token,
        "new_password": "Test@123",
        "confirm_password": "Test@123",
    }
    response = client.post(
        get_verify_user_url,
        post_invite_user_data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "新規ユーザの認証に成功しました"}
    assert User.objects.get(id=user.id).is_verified
    assert UserInvitation.objects.get(id=invitation.id).is_used


@pytest.mark.django_db
def test_cannot_verify_user_without_token(
    client,
    management_user,
    password,
    get_verify_user_url,
):
    """管理者がシステムユーザを作成(認証)できることを確認"""
    client.login(
        employee_number=management_user.employee_number,
        password=password,
    )
    user = UserFactory(is_verified=False)
    invitation = UserInvitationFactory(
        user=user,
    )
    post_invite_user_data = {
        "token": invitation.token,
        "new_password": "Test@123",
        "confirm_password": "Test@123",
    }
    UserInvitation.objects.filter(id=invitation.id).delete()
    response = client.post(
        get_verify_user_url,
        post_invite_user_data,
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"msg": "有効期限切れのリンクです。管理者に再送信を依頼してください"}


@pytest.mark.django_db
def test_cannot_verify_user_token_with_expired_token(
    client,
    management_user,
    password,
    get_verify_user_url,
):
    """招待用トークンの有効期限が切れたら認証できないことをテスト"""
    client.login(
        employee_number=management_user.employee_number,
        password=password,
    )
    user = UserFactory(is_verified=False)
    invitation = UserInvitationFactory(
        user=user,
    )
    post_invite_user_data = {
        "token": invitation.token,
        "new_password": "Test@123",
        "confirm_password": "Test@123",
    }
    expiry_time = timezone.localtime() + timedelta(days=1, minutes=1)
    with freeze_time(expiry_time):
        response = client.post(
            get_verify_user_url,
            post_invite_user_data,
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"msg": "有効期限切れのリンクです。管理者に再送信を依頼してください"}
        assert not User.objects.get(id=user.id).is_verified
        assert not UserInvitation.objects.get(id=invitation.id).is_used
