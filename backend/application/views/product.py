from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from application.models import Product
from application.serializers.product import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
