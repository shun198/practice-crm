from rest_framework import serializers

from application.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """ユーザ用シリアライザ"""

    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["id"]

    def to_representation(self, instance):
        rep = super(CustomerSerializer, self).to_representation(instance)
        rep["address"] = (
            instance.address.prefecture
            + instance.address.municipalities
            + instance.address.house_no
            + instance.address.other
        )
        rep["post_no"] = instance.address.post_no
        return rep
