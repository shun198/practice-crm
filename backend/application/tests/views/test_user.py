import pytest
from rest_framework import status

from application.tests.common_method import login


@pytest.fixture
def get_user_url():
    return "/api/users/"


def get_user_details_url(id):
    return f"/api/users/{id}/"


@pytest.mark.django_db
def test_management_user_can_list_users(
    client, login_management, get_user_url
):
    """管理者ユーザでユーザの一覧を表示できるテスト"""
    login(client, login_management)
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_general_user_can_list_users(client, login_management, get_user_url):
    """一般ユーザでユーザの一覧を表示できるテスト"""
    login(client, login_management)
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_sales_user_can_list_users(client, login_part_time, get_user_url):
    """アルバイトユーザでユーザの一覧を表示できるテスト"""
    login(client, login_part_time)
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cannot_list_users_without_login(client, get_user_url):
    """ログインなしでユーザの一覧を表示できないテスト"""
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
