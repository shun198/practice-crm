"""DI定義用のモジュール"""
import boto3
from application.utils.sms import SnsResource, SnsWrapper
from injector import Binder, Injector, Module
from project.settings.environment import aws_settings


class SnsWrapperModule(Module):
    def configure(self, binder):
        binder.bind(SnsWrapper)


class LocalSnsModule(Module):
    """Local環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        sns_resource = SnsResource(
            boto3.resource(
                "sns",
                region_name=aws_settings.AWS_DEFAULT_REGION_NAME,
                endpoint_url=aws_settings.ENDPOINT_URL,
            )
        )
        binder.bind(SnsResource, to=sns_resource)


class DevSnsModule(Module):
    """Dev環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        sns_resource = SnsResource(
            boto3.resource("sns", region_name=aws_settings.AWS_DEFAULT_REGION_NAME)
        )
        binder.bind(SnsResource, to=sns_resource)


injector = Injector([SnsWrapperModule()])
