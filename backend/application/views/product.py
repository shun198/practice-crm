from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from application.models import Product
from application.permissions import IsGeneralUser
from application.serializers.product import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsGeneralUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "price"
