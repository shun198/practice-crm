"""DI定義用のモジュール"""
import boto3
from application.utils.s3 import S3BucketResource, S3BucketWrapper
from injector import Binder, Injector, Module
from project.settings.environment import aws_settings


class S3BucketWrapperModule(Module):
    """S3BucketのWrapper用のモジュール"""

    def configure(self, binder: Binder) -> None:
        binder.bind(S3BucketWrapper)
        return super().configure(binder)


class LocalS3Module(Module):
    """Local環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        s3_resource = S3BucketResource(
            boto3.client(
                "s3", region_name=aws_settings.AWS_DEFAULT_REGION_NAME,endpoint_url=aws_settings.ENDPOINT_URL,
            )
        )
        binder.bind(S3BucketResource, to=s3_resource)


class DevS3Module(Module):
    """Dev環境用のモジュール"""

    def configure(self, binder: Binder) -> None:
        s3_resource = S3BucketResource(
            boto3.client(
                "s3", region_name=aws_settings.AWS_DEFAULT_REGION_NAME
            )
        )
        binder.bind(S3BucketResource, to=s3_resource)


s3_injector = Injector([S3BucketWrapperModule()])
"""DI用のコンテナ"""
