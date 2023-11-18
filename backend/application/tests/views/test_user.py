import pytest
from rest_framework import status

from application.models.user import User
from application.tests.factories.user import UserFactory


@pytest.fixture
def get_user_url():
    return "/api/users/"


def get_user_details_url(id):
    return f"/api/users/{id}/"


@pytest.fixture
def user_data():
    return {
        "employee_number": "11111111",
        "username": "テストユーザ01",
        "email": "test_user_01@test.com",
        "role": User.Role.MANAGEMENT,
    }


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


@pytest.mark.django_db
def test_management_user_can_list_user_details(
    client, management_user, user_password
):
    """管理者ユーザでユーザの詳細を表示できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=management_user.employee_number, password=user_password
    )
    response = client.get(get_user_details_url(user.id), format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_general_user_can_list_user_details(
    client, general_user, user_password
):
    """一般ユーザでユーザの詳細を表示できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=general_user.employee_number, password=user_password
    )
    response = client.get(get_user_details_url(user.id), format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_part_time_user_can_list_user_details(
    client, part_time_user, user_password
):
    """アルバイトユーザでユーザの詳細を表示できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=part_time_user.employee_number, password=user_password
    )
    response = client.get(get_user_details_url(user.id), format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_management_user_can_create_user(
    client, management_user, user_password, get_user_url, user_data
):
    """管理者ユーザでユーザを作成できるテスト"""
    client.login(
        employee_number=management_user.employee_number, password=user_password
    )
    response = client.post(get_user_url, user_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_general_user_cannot_create_user(
    client, general_user, user_password, get_user_url, user_data
):
    """一般ユーザでユーザを作成できないテスト"""
    client.login(
        employee_number=general_user.employee_number, password=user_password
    )
    response = client.post(get_user_url, user_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_general_user_cannot_create_user(
    client, part_time_user, user_password, get_user_url, user_data
):
    """アルバイトユーザでユーザを作成できないテスト"""
    client.login(
        employee_number=part_time_user.employee_number, password=user_password
    )
    response = client.post(get_user_url, user_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_management_user_can_update_user(
    client, management_user, user_password, user_data
):
    """管理者ユーザでユーザを更新できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=management_user.employee_number, password=user_password
    )
    response = client.put(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_general_user_cannot_update_user(
    client, general_user, user_password, user_data
):
    """一般ユーザでユーザを更新できないテスト"""
    user = UserFactory()
    client.login(
        employee_number=general_user.employee_number, password=user_password
    )
    response = client.put(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_general_user_cannot_update_user(
    client, part_time_user, user_password, user_data
):
    """アルバイトユーザでユーザを更新できないテスト"""
    user = UserFactory()
    client.login(
        employee_number=part_time_user.employee_number, password=user_password
    )
    response = client.put(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_management_user_can_partial_update_user(
    client, management_user, user_password, user_data
):
    """管理者ユーザでユーザを一部更新できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=management_user.employee_number, password=user_password
    )
    response = client.patch(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_general_user_cannot_partial_update_user(
    client, general_user, user_password, user_data
):
    """一般ユーザでユーザを一部更新できないテスト"""
    user = UserFactory()
    client.login(
        employee_number=general_user.employee_number, password=user_password
    )
    response = client.patch(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_general_user_cannot_partial_update_user(
    client, part_time_user, user_password, user_data
):
    """アルバイトユーザでユーザを一部更新できないテスト"""
    user = UserFactory()
    client.login(
        employee_number=part_time_user.employee_number, password=user_password
    )
    response = client.patch(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_management_user_can_delete_user(
    client, management_user, user_password, user_data
):
    """管理者ユーザでユーザを削除できるテスト"""
    user = UserFactory()
    client.login(
        employee_number=management_user.employee_number, password=user_password
    )
    response = client.delete(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_general_user_cannot_delete_user(
    client, general_user, user_password, user_data
):
    """一般ユーザでユーザを削除できないテスト"""
    user = UserFactory()
    client.login(
        employee_number=general_user.employee_number, password=user_password
    )
    response = client.delete(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_general_user_cannot_delete_user(
    client, part_time_user, user_password, user_data
):
    """アルバイトユーザでユーザを削除できないテスト"""
    user = UserFactory()
    client.login(
        employee_number=part_time_user.employee_number, password=user_password
    )
    response = client.delete(
        get_user_details_url(user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_cannot_delete_yourself(
    client, management_user, user_password, user_data
):
    """自身を削除できないテスト"""
    client.login(
        employee_number=management_user.employee_number, password=user_password
    )
    response = client.delete(
        get_user_details_url(management_user.id), user_data, format="json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"msg": "自身を削除する事は出来ません"}
