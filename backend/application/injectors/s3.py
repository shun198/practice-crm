"""DI定義用のモジュール"""
import boto3
from application.utils.s3 import S3BucketResource, S3BucketWrapper
from injector import Binder, Injector, Module
from project.settings.environment import aws_settings


class S3BucketWrapperModule(Module):
    """S3BucketのWrapper用のモジュール"""

    def configure(self, binder: Binder) -> None:
        binder.bind(S3BucketWrapper)


class LocalSesModule(Module):
    """Local環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        ses_resource = S3BucketResource(
            boto3.resource(
                "s3", region_name=aws_settings.AWS_DEFAULT_REGION_NAME
            )
        )
        binder.bind(S3BucketResource, to=ses_resource)


class DevSesModule(Module):
    """Dev環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        ses_resource = S3BucketResource(
            boto3.resource(
                "s3", region_name=aws_settings.AWS_DEFAULT_REGION_NAME
            )
        )
        binder.bind(S3BucketResource, to=ses_resource)


s3_injector = Injector([S3BucketWrapperModule()])
"""DI用のコンテナ"""
