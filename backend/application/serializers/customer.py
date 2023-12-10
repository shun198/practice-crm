from application.models import Customer
from django.utils import timezone
from rest_framework import serializers


class ListCustomerSerializer(serializers.ModelSerializer):
    """ユーザ詳細表示用シリアライザ"""

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "kana",
            "email",
            "phone_no",
            "created_at",
            "updated_by",
        ]
        read_only_fields = ["id", "created_at","updated_by",]

    def to_representation(self, instance):
        rep = super(ListCustomerSerializer, self).to_representation(instance)
        rep["created_at"] = timezone.localtime(instance.created_at).strftime("%Y/%m/%d")
        rep["updated_by"] = instance.updated_by.username
        return rep


class DetailCustomerSerializer(serializers.ModelSerializer):
    """ユーザ詳細表示用シリアライザ"""

    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["id"]

    def to_representation(self, instance):
        rep = super(DetailCustomerSerializer, self).to_representation(instance)
        rep["address"] = (
            instance.address.prefecture
            + instance.address.municipalities
            + instance.address.house_no
            + instance.address.other
        )
        rep["post_no"] = instance.address.post_no
        rep["created_by"] = instance.created_by.username
        rep["updated_by"] = instance.updated_by.username
        return rep
