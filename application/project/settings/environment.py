"""環境変数定義用のモジュール"""

from pydantic import BaseSettings


class DjangoSettings(BaseSettings):
    """Django関連の環境変数を設定するクラス"""

    SECRET_KEY: str
    ALLOWED_HOSTS: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str = "db"
    MYSQL_PORT: int = 3306


class AwsSettings(BaseSettings):
    """AWS関連の環境変数を設定するクラス"""

    AWS_REGION_NAME: str = "ap-northeast-1"
    ENDPOINT_URL: str = "http://localstack:4566"
    AWS_DEFAULT_REGION_NAME: str = "ap-northeast-1"
    AWS_SES_REGION_ENDPOINT: str = "ap-northeast-1"
    AWS_STORAGE_BUCKET_NAME: str = "localstack"
    DEFAULT_FROM_EMAIL: str = "example@gmail.com"
    AWS_PROFILE: str = "localstack"


django_settings = DjangoSettings()


aws_settings = AwsSettings()
