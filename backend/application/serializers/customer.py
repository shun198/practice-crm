from django.utils import timezone
from rest_framework import serializers

from application.models import Address, Customer, Photo
from application.utils.fields import CustomFileField


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
        read_only_fields = [
            "id",
            "created_at",
            "updated_by",
        ]

    def to_representation(self, instance):
        rep = super(ListCustomerSerializer, self).to_representation(instance)
        rep["created_at"] = timezone.localtime(instance.created_at).strftime(
            "%Y/%m/%d"
        )
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


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "kana",
            "email",
            "phone_no",
            "birthday",
        ]
        read_only_fields = ["id"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["id"]


class CreateAndUpdateCustomerSerializer(serializers.Serializer):
    customer = CustomerSerializer()
    address = AddressSerializer()

    def to_representation(self, instance: Customer):
        try:
            customer = CustomerSerializer(instance).data
        except AttributeError:
            customer = {}
        try:
            address = AddressSerializer(instance.address).data
        except AttributeError:
            address = {}
        rep = {
            "customer": customer,
            "address": address,
        }
        return rep


class ImportCsvSerializer(serializers.Serializer):
    """CSVインポート用のシリアライザ"""

    file = serializers.FileField()


class CustomerPhotoSerializer(serializers.ModelSerializer):
    photo = CustomFileField()

    class Meta:
        model = Photo
        fields = ["id", "photo", "created_at", "created_by"]
        read_only_fields = ["id", "created_at", "created_by"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["photo"] = instance.photo.name.split("/")[-1]
        rep["created_by"] = instance.created_by.username
        return rep
