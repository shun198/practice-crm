from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from application.filters import CustomerFilter
from application.models import Customer
from application.serializers.customer import (
    DetailCustomerSerializer,
    ListCustomerSerializer,
)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related("address")
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = CustomerFilter

    def get_serializer_class(self):
        match self.action:
            case "list":
                return ListCustomerSerializer
            case "retrieve":
                return DetailCustomerSerializer
            case _:
                return None
