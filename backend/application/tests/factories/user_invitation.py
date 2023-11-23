import secrets
from datetime import timedelta

import factory
from django.utils import timezone

from application.models import UserInvitation
from application.tests.factories.user import UserFactory


class UserInvitationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserInvitation

    user = factory.SubFactory(UserFactory)
    token = secrets.token_urlsafe(64)
    expiry = timezone.localtime() + timedelta(days=1)
    is_used = False
