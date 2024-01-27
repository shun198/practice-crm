from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework import status

from application.tests.factories.customer import CustomerFactory


def get_send_sms_url(id):
    return f"/api/customers/{id}/send_sms"


@pytest.mark.django_db
def test_management_user_can_send_sms(
    client,
    management_user,
    password,
):
    """管理者ユーザがお客様へSMSを送信できるテスト"""
    client.login(
        employee_number=management_user.employee_number, password=password
    )
    customer = CustomerFactory()
    response = client.post(get_send_sms_url(id=customer.id), format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "SMSの送信に成功しました"}
