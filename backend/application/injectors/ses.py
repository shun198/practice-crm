"""DI定義用のモジュール"""
import boto3
from application.utils.ses import SESWrapper
from botocore.client import BaseClient
from injector import Binder, Injector, Module
from project.settings.environment import aws_settings


class SESWrappereModule(Module):
    """SESWrapper用のモジュール"""

    def configure(self, binder: Binder) -> None:
        binder.bind(SESWrapper)
        return super().configure(binder)


class LocalModule(Module):
    """ローカル環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        client = boto3.client(
            "ses",
            region_name=aws_settings.AWS_DEFAULT_REGION_NAME,
            endpoint_url=aws_settings.ENDPOINT_URL,
        )
        client.verify_email_identity(EmailAddress=aws_settings.SENDER)
        binder.bind(BaseClient, to=client)
        return super().configure(binder)


class PrdModule(Module):
    """本番環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        binder.bind(
            BaseClient, to=boto3.client("ses", region_name=aws_settings.AWS_DEFAULT_REGION_NAME)
        )
        return super().configure(binder)


injector = Injector([SESWrappereModule()])
"""DI用のコンテナ"""