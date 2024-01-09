import pytest
from rest_framework import status


@pytest.fixture
def get_login_url():
    return "/api/login"


@pytest.fixture
def get_logout_url():
    return "/api/logout"


@pytest.mark.django_db
def test_management_user_can_login(
    client, management_user, password, get_login_url
):
    """管理者ユーザで正常にログインできることをテスト"""
    response = client.post(
        get_login_url,
        {
            "employee_number": management_user.employee_number,
            "password": password,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "username": management_user.username,
        "group": management_user.group.name,
    }


@pytest.mark.django_db
def test_general_user_can_login(client, general_user, password, get_login_url):
    """一般ユーザで正常にログインできることをテスト"""
    response = client.post(
        get_login_url,
        {
            "employee_number": general_user.employee_number,
            "password": password,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "username": general_user.username,
        "group": general_user.group.name,
    }


@pytest.mark.django_db
def test_user_cannot_login_with_incorrect_password(
    client, management_user, get_login_url
):
    """間違ったパスワードでログインできないことをテスト"""
    response = client.post(
        get_login_url,
        {
            "employee_number": management_user.employee_number,
            "password": "wrong_password",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"msg": "社員番号またはパスワードが間違っています"}


@pytest.mark.django_db
def test_user_cannot_login_without_password(
    client, management_user, get_login_url
):
    """パスワードなしでログインできないことをテスト"""
    response = client.post(
        get_login_url,
        {
            "employee_number": management_user.employee_number,
            "password": None,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_cannot_login_without_employee_number(
    client, password, get_login_url
):
    """社員番号なしでログインできないことをテスト"""
    response = client.post(
        get_login_url,
        {
            "employee_number": None,
            "password": password,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_cannot_login_with_employee_number_that_does_not_exist(
    client, password, get_login_url
):
    """存在しない社員番号でログインできないことをテスト"""
    response = client.post(
        get_login_url,
        {
            "employee_number": "12345678",
            "password": password,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_can_logout(client, management_user, password, get_logout_url):
    """正常にログアウトできることをテスト"""
    response = client.post(
        get_login_url,
        {
            "employee_number": management_user.employee_number,
            "password": password,
        },
        format="json",
    )
    response = client.post(get_logout_url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cannot_logout_without_login(client, get_logout_url):
    """ログインしていなくても200を返すことをテスト"""
    response = client.post(get_logout_url, format="json")
    assert response.status_code == status.HTTP_200_OK
