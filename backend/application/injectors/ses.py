"""DI定義用のモジュール"""
import boto3
from application.utils.ses import SesResource, SesWrapper
from injector import Binder, Injector, Module
from project.settings.environment import aws_settings


class SesWrapperModule(Module):
    """SesWrapper用のモジュール"""

    def configure(self, binder: Binder) -> None:
        binder.bind(SesWrapper)


class LocalSesModule(Module):
    """Local環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        ses_resource = SesResource(
            boto3.resource(
                "ses", region_name=aws_settings.AWS_DEFAULT_REGION_NAME
            )
        )
        binder.bind(SesResource, to=ses_resource)


class DevSesModule(Module):
    """Dev環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        ses_resource = SesResource(
            boto3.resource(
                "sns", region_name=aws_settings.AWS_DEFAULT_REGION_NAME
            )
        )
        binder.bind(SesResource, to=ses_resource)


ses_injector = Injector([SesWrapperModule()])
"""DI用のコンテナ"""
