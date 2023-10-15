from application.models import Product
from application.permissions import IsGeneralUser
from application.serializers.product import ProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsGeneralUser]
