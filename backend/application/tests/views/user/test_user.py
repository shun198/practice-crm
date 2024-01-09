import pytest
from rest_framework import status

from application.tests.factories.user import UserFactory
from application.utils.constants import Group


@pytest.fixture
def get_user_url():
    return "/api/users"


def get_user_details_url(id):
    return f"/api/users/{id}"


@pytest.fixture
def user_data():
    return {
        "employee_number": "11111111",
        "username": "テストユーザ01",
        "email": "test_user_01@test.com",
        "group": Group.MANAGER.value,
    }


@pytest.mark.django_db
def test_management_user_can_list_users(
    client, management_user, password, get_user_url
):
    """管理者ユーザでユーザの一覧を表示できるテスト"""
    client.login(
        employee_number=management_user.employee_number, password=password
    )
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_general_user_can_list_users(
    client, general_user, password, get_user_url
):
    """一般ユーザでユーザの一覧を表示できるテスト"""
    client.login(
        employee_number=general_user.employee_number, password=password
    )
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cannot_list_users_without_login(client, get_user_url):
    """ログインなしでユーザの一覧を表示できないテスト"""
    response = client.get(get_user_url, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_management_user_can_list_user_details(
    client, management_user, password
):
    """管理者ユーザでユーザの詳細を表示できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=management_user.employee_number, password=password
    )
    response = client.get(get_user_details_url(user.id), format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_general_user_can_list_user_details(client, general_user, password):
    """一般ユーザでユーザの詳細を表示できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=general_user.employee_number, password=password
    )
    response = client.get(get_user_details_url(user.id), format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_management_user_can_create_user(
    client, management_user, password, get_user_url, user_data
):
    """管理者ユーザでユーザを作成できるテスト"""
    client.login(
        employee_number=management_user.employee_number, password=password
    )
    response = client.post(get_user_url, user_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_general_user_cannot_create_user(
    client, general_user, password, get_user_url, user_data
):
    """一般ユーザでユーザを作成できないテスト"""
    client.login(
        employee_number=general_user.employee_number, password=password
    )
    response = client.post(get_user_url, user_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_management_user_can_update_user(
    client, management_user, password, user_data
):
    """管理者ユーザでユーザを更新できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=management_user.employee_number, password=password
    )
    response = client.put(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_general_user_cannot_update_user(
    client, general_user, password, user_data
):
    """一般ユーザでユーザを更新できないテスト"""
    user = UserFactory()
    client.login(
        employee_number=general_user.employee_number, password=password
    )
    response = client.put(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_management_user_can_partial_update_user(
    client, management_user, password, user_data
):
    """管理者ユーザでユーザを一部更新できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=management_user.employee_number, password=password
    )
    response = client.patch(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_general_user_cannot_partial_update_user(
    client, general_user, password, user_data
):
    """一般ユーザでユーザを一部更新できないテスト"""
    user = UserFactory()
    client.login(
        employee_number=general_user.employee_number, password=password
    )
    response = client.patch(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_management_user_can_delete_user(
    client, management_user, password, user_data
):
    """管理者ユーザでユーザを削除できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=management_user.employee_number, password=password
    )
    response = client.delete(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_general_user_cannot_delete_user(
    client, general_user, password, user_data
):
    """一般ユーザでユーザを削除できないテスト"""
    user = UserFactory()
    client.login(
        employee_number=general_user.employee_number, password=password
    )
    response = client.delete(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_cannot_delete_yourself(
    client, management_user, password, user_data
):
    """自身を削除できないテスト"""
    client.login(
        employee_number=management_user.employee_number, password=password
    )
    response = client.delete(
        get_user_details_url(management_user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"msg": "自身を削除する事は出来ません"}
