import pytest
from rest_framework import status

from application.tests.common_method import login


@pytest.fixture
def get_login_url():
    return "/api/login/"


@pytest.fixture
def get_logout_url():
    return "/api/logout/"


@pytest.mark.django_db
def test_management_user_can_login(client, login_management, get_login_url):
    """管理者ユーザで正常にログインできることをテスト"""
    response = client.post(get_login_url, login_management, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"role": "MANAGEMENT"}


@pytest.mark.django_db
def test_general_user_can_login(client, login_general, get_login_url):
    """一般ユーザで正常にログインできることをテスト"""
    response = client.post(get_login_url, login_general, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"role": "GENERAL"}


@pytest.mark.django_db
def test_part_time_user_can_login(client, login_part_time, get_login_url):
    """アルバイトユーザで正常にログインできることをテスト"""
    response = client.post(get_login_url, login_part_time, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"role": "PART_TIME"}


@pytest.mark.django_db
def test_user_cannot_login_with_incorrect_password(
    client, login_management, get_login_url
):
    """間違ったパスワードでログインできないことをテスト"""
    login_management["password"] = "test6789"
    response = client.post(get_login_url, login_management, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "msg": "either employee number or password is incorrect"
    }


@pytest.mark.django_db
def test_user__cannot_login_with_incorrect_password(
    client, login_management, get_login_url
):
    """間違ったパスワードでログインできないことをテスト"""
    login_management["password"] = "test6789"
    response = client.post(get_login_url, login_management, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "msg": "either employee number or password is incorrect"
    }


@pytest.mark.django_db
def test_user_cannot_login_without_password(
    client, login_management, get_login_url
):
    """パスワードなしでログインできないことをテスト"""
    login_management["password"] = None
    response = client.post(get_login_url, login_management, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_cannot_login_without_employee_number(
    client, login_management, get_login_url
):
    """社員番号なしでログインできないことをテスト"""
    login_management["employee_number"] = None
    response = client.post(get_login_url, login_management, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_cannot_login_with_employee_number_that_does_not_exist(
    client, login_management, get_login_url
):
    """存在しない社員番号でログインできないことをテスト"""
    login_management["employee_number"] = "12345678"
    response = client.post(get_login_url, login_management, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_can_logout(client, login_management, get_login_url):
    """正常にログアウトできることをテスト"""
    login(client, login_management)
    response = client.post(get_login_url, login_management, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cannot_logout_without_login(
    client, login_management, get_login_url
):
    """ログインしていなくても200を返すことをテスト"""
    response = client.post(get_login_url, login_management, format="json")
    assert response.status_code == status.HTTP_200_OK
