import pytest
from django.core.management import call_command
from rest_framework.test import APIClient
from application.tests.factories.user import UserFactory
from application.models.user import User


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "fixture.json")


@pytest.fixture
def login_management():
    return {
        "employee_number": "00000001",
        "password": "test",
    }


@pytest.fixture
def login_general():
    return {
        "employee_number": "00000002",
        "password": "test",
    }


@pytest.fixture
def login_part_time():
    return {
        "employee_number": "00000003",
        "password": "test",
    }


@pytest.fixture
def client(scope="session"):
    return APIClient()


@pytest.fixture
def management_user(user_password):
    return UserFactory(
        password=user_password,
        role=User.Role.MANAGEMENT,
    )


@pytest.fixture
def general_user(user_password):
    return UserFactory(
        password=user_password,
        role=User.Role.GENERAL,
    )

@pytest.fixture
def part_time_user(user_password):
    return UserFactory(
        password=user_password,
        role=User.Role.PART_TIME,
    )

@pytest.fixture
def user_password():
    return "test"