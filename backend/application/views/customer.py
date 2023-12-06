from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from application.filters import CustomerFilter
from application.models import Customer
from application.serializers.customer import CustomerSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related("address")
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = CustomerFilter
