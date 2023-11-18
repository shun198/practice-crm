import pytest
from rest_framework import status


@pytest.fixture
def get_user_url():
    return "/api/users/"


def get_user_details_url(id):
    return f"/api/users/{id}/"


@pytest.mark.django_db
def test_management_user_can_list_users(
    client, management_user, user_password, get_user_url
):
    """管理者ユーザでユーザの一覧を表示できるテスト"""
    client.login(
        employee_number=management_user.employee_number, password=user_password
    )
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_general_user_can_list_users(
    client, general_user, user_password, get_user_url
):
    """一般ユーザでユーザの一覧を表示できるテスト"""
    client.login(
        employee_number=general_user.employee_number, password=user_password
    )
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_sales_user_can_list_users(
    client, part_time_user, user_password, get_user_url
):
    """アルバイトユーザでユーザの一覧を表示できるテスト"""
    client.login(
        employee_number=part_time_user.employee_number, password=user_password
    )
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cannot_list_users_without_login(client, get_user_url):
    """ログインなしでユーザの一覧を表示できないテスト"""
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
