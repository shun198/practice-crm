from rest_framework import serializers

from application.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """商品用シリアライザ"""

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
