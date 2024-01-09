import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from application.models.user import User
from application.tests.factories.user import UserFactory
from application.utils.constants import Group


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "fixture.json")


@pytest.fixture
def client(scope="session"):
    return APIClient()


@pytest.fixture
def management_user(password):
    return UserFactory(
        password=password,
        group_id=Group.MANAGER.value,
    )


@pytest.fixture
def general_user(password):
    return UserFactory(
        password=password,
        group_id=Group.GENERAL.value,
    )


@pytest.fixture
def password():
    return "test"
