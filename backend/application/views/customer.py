import csv
import tempfile
from logging import getLogger

import chardet
from django.db import DatabaseError, transaction
from django.http import FileResponse, JsonResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from application.filters import CustomerFilter
from application.models import Address, Customer, Photo
from application.serializers.customer import (
    AddressSerializer,
    CreateAndUpdateCustomerSerializer,
    CustomerPhotoSerializer,
    CustomerSerializer,
    DetailCustomerSerializer,
    ImportCsvSerializer,
    ListCustomerSerializer,
)
from application.utils.logs import LoggerName


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related("address")
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = CustomerFilter
    application_logger = getLogger(LoggerName.APPLICATION.value)

    def get_serializer_class(self):
        match self.action:
            case "list":
                return ListCustomerSerializer
            case "retrieve":
                return DetailCustomerSerializer
            case "create" | "update" | "partial_update":
                return CreateAndUpdateCustomerSerializer
            case "csv_import":
                return ImportCsvSerializer
            case _:
                return None

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """お客様情報作成用API

        Args:
            request : リクエスト

        Returns:
            JsonResponse
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            address = Address.objects.create(
                **serializer.validated_data.get("address"),
            )
            customer = Customer.objects.create(
                **serializer.validated_data.get("customer"),
                address=address,
                created_by=request.user,
                updated_by=request.user,
            )
            response_data = {
                "customer": CustomerSerializer(instance=customer).data,
                "address": AddressSerializer(instance=address).data,
            }
            return JsonResponse(
                response_data,
                status=status.HTTP_201_CREATED,
            )
        except DatabaseError as e:
            self.application_logger.warning(e)
            return JsonResponse(
                data={"msg": "お客様情報の作成に失敗しました"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """お客様情報更新用API

        Args:
            request : リクエスト

        Returns:
            Union[
                Response,
                JsonResponse
            ]
        """
        try:
            partial = kwargs.pop("partial", False)
            customer = self.get_object()
            serializer = self.get_serializer(
                customer, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            if request.data.get("address") is not None:
                address_serializer = AddressSerializer(
                    customer.address,
                    data=request.data.get("address"),
                    context=self.get_serializer_context(),
                )
                address_serializer.is_valid(raise_exception=True)
                address_serializer.save()
            if request.data.get("customer") is not None:
                customer_serializer = CustomerSerializer(
                    customer,
                    data=request.data.get("customer"),
                    context=self.get_serializer_context(),
                )
                customer_serializer.is_valid(raise_exception=True)
                customer_serializer.save()
            return Response(serializer.data)
        except DatabaseError as e:
            self.application_logger.warning(e)
            return JsonResponse(
                data={"msg": "お客様情報の更新に失敗しました"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @transaction.atomic
    @action(methods=["post"], detail=False)
    def csv_import(self, request):
        """お客様一括登録API

        CSVファイルを読み込み、お客様を一括で登録する

        Returns:
            Response
        """
        file = request.FILES.get("file")
        encoding = chardet.detect(file.read())
        file.seek(0)
        if encoding["encoding"] != "utf-8":
            return JsonResponse(
                data={"msg": "CSVファイルのエンコードをutf-8にしてください"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        decoded_file = file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)
        next(reader)
        for row in reader:
            try:
                address_data = {
                    "prefecture": row[5],
                    "municipalities": row[6],
                    "house_no": row[7],
                    "other": row[8],
                    "post_no": row[9],
                }
                customer_data = {
                    "name": row[0],
                    "kana": row[1],
                    "birthday": row[2],
                    "email": row[3],
                    "phone_no": "0" + row[4],
                }
                address_serializer = AddressSerializer(data=address_data)
                address_serializer.is_valid(raise_exception=True)
                customer_serializer = CustomerSerializer(data=customer_data)
                customer_serializer.is_valid(raise_exception=True)
                address = Address.objects.create(
                    **address_data,
                )
                Customer.objects.create(
                    **customer_data,
                    address=address,
                    created_by=request.user,
                    updated_by=request.user,
                )
            except BaseException as e:
                self.application_logger.warning(e)
                return JsonResponse(data={"msg": f"csvファイルのimportに失敗しました。"})
        return JsonResponse(data={"msg": "csvファイルのimportに成功しました"})

    @action(methods=["get"], detail=False)
    def csv_export(self, request):
        """お客様一覧のCSVをエクスポートする用のAPI

        Args:
            request : リクエスト

        Returns:
            CSVファイル
        """
        queryset = self.filter_queryset(self.get_queryset())
        file = self._create_export_customer_csv(queryset)
        filename = (
            "お客様データ＿" + timezone.localdate().strftime("%Y-%m-%d") + ".csv"
        )
        response = FileResponse(
            open(file.name, "rb"),
            as_attachment=True,
            content_type="application/csv",
            filename=filename,
        )
        return response

    def _create_export_customer_csv(self, customers):
        """エクスポートするCSVを作成するプライベートメソッド

        Args:
            customers : Customerのqueryset

        Returns:
            file: CSVファイル
        """
        file = tempfile.NamedTemporaryFile(delete=False)
        with open(file.name, "w") as csvfile:
            fieldnames = [
                "氏名",
                "カナ氏名",
                "誕生日",
                "メールアドレス",
                "電話番号",
                "作成日",
                "担当者",
                "都道府県",
                "市区町村",
                "丁・番地",
                "その他(マンション名など)",
                "郵便番号",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for customer in customers:
                writer.writerow(
                    {
                        "氏名": customer.name,
                        "カナ氏名": customer.kana,
                        "誕生日": customer.birthday,
                        "メールアドレス": customer.email,
                        "電話番号": customer.phone_no,
                        "作成日": timezone.localdate(
                            customer.created_at
                        ).strftime("%Y/%m/%d"),
                        "担当者": customer.updated_by.username,
                        "都道府県": customer.address.prefecture,
                        "市区町村": customer.address.municipalities,
                        "丁・番地": customer.address.house_no,
                        "その他(マンション名など)": customer.address.other,
                        "郵便番号": customer.address.post_no,
                    }
                )
        # ストリーム位置をリセット
        # ファイルの読み取り/書き込み位置をファイルの先頭に戻す
        file.seek(0)
        return file


class CustomerPhotoViewSet(ModelViewSet):
    queryset = Photo.objects.select_related("customer")
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerPhotoSerializer

    def create(self, request, *args, **kwargs):
        photo_data = []
        for photo in request.FILES.getlist("photo"):
            serializer = self.get_serializer(data={"photo": photo})
            serializer.is_valid(raise_exception=True)
            photo_data.append(
                Photo.objects.create(
                    customer_id=kwargs["customer_pk"],
                    photo=photo,
                    created_by=request.user,
                )
            )
        response = self.serializer_class(photo_data, many=True).data
        return Response(response, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.photo.delete(save=False)
        instance.delete()
