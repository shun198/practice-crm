import pytest
from django.core.management import call_command
from rest_framework.test import APIClient


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
def email_data():
    return {
        "email": "test_user_01@test.com",
    }


@pytest.fixture
def client(scope="session"):
    return APIClient()
