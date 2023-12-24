import pytest
from django.core import mail
from django.db import DatabaseError
from rest_framework import status

from application.models import User, UserInvitation
from application.tests.common_method import mail_confirm


@pytest.fixture
def get_invite_user_url():
    """社員招待用のurl"""
    return "/api/users/invite_user"


@pytest.fixture
def post_invite_user_data():
    """社員招待用のインプットデータ"""
    return {
        "employee_number": "99999990",
        "name": "テストユーザ01",
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


@pytest.mark.django_db
def test_invite_user_save_user_transaction_database_error_false(
    mocker,
    client,
    management_user,
    password,
    get_invite_user_url,
    post_invite_user_data,
):
    """Userモデル保存時にトランザクション処理が失敗した場合、DBに保存されずにFalseが返ってくる事を確認する"""
    client.login(
        employee_number=management_user.employee_number, password=password
    )
    # Userモデルのsaveメソッドを実行すると、常にDatabaseErrorを発生させる
    mocker.patch.object(User, "save", side_effect=DatabaseError)
    response = client.post(
        get_invite_user_url,
        post_invite_user_data,
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not User.objects.filter(
        employee_number=post_invite_user_data["employee_number"]
    ).exists()
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_invite_user_save_user_invitation_transaction_database_error_false(
    mocker,
    client,
    management_user,
    password,
    get_invite_user_url,
    post_invite_user_data,
):
    """UserInvitationモデル保存時にトランザクション処理が失敗した場合、DBに保存されずにFalseが返ってくる事を確認する"""
    client.login(
        employee_number=management_user.employee_number, password=password
    )
    # UserInvitationモデルのsaveメソッドを実行すると、常にDatabaseErrorを発生させる
    mocker.patch.object(UserInvitation, "save", side_effect=DatabaseError)
    response = client.post(
        get_invite_user_url,
        post_invite_user_data,
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not User.objects.filter(
        employee_number=post_invite_user_data["employee_number"]
    ).exists()
    assert len(mail.outbox) == 0
