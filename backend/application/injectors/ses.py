"""DI定義用のモジュール"""
import boto3
from application.utils.ses import SesResource, SesWrapper
from botocore.client import BaseClient
from injector import Binder, Injector, Module
from project.settings.environment import aws_settings


class SesWrapperModule(Module):
    """SesWrapper用のモジュール"""

    def configure(self, binder: Binder) -> None:
        binder.bind(SesWrapper)
        return super().configure(binder)


class LocalSesModule(Module):
    """Local環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        client = boto3.client(
            "ses",
            region_name=aws_settings.AWS_DEFAULT_REGION_NAME,
            endpoint_url=aws_settings.ENDPOINT_URL,
        )
        client.verify_email_identity(EmailAddress=aws_settings.SENDER)
        binder.bind(BaseClient, to=client)
        return super().configure(binder)


class DevSesModule(Module):
    """Dev環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        ses_resource = SesResource(
            boto3.client(
                BaseClient, "ses", region_name=aws_settings.AWS_DEFAULT_REGION_NAME
            )
        )
        binder.bind(SesResource, to=ses_resource)
        return super().configure(binder)


ses_injector = Injector([SesWrapperModule()])
"""DI用のコンテナ"""
