import secrets
from datetime import timedelta

import factory
from django.utils import timezone

from application.models import UserResetPassword
from application.tests.factories.user import UserFactory


class UserResetPasswordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserResetPassword

    user = factory.SubFactory(UserFactory)
    token = secrets.token_urlsafe(64)
    expiry = timezone.localtime() + timedelta(minutes=30)
    is_used = False
