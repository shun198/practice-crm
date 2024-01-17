"""環境変数定義用のモジュール"""

from pydantic import BaseSettings


class DjangoSettings(BaseSettings):
    """Django関連の環境変数を設定するクラス"""

    SECRET_KEY: str = "secretkey"
    ALLOWED_HOSTS: str = "localhost 127.0.0.1 [::1] back web"
    POSTGRES_NAME: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    TRUSTED_ORIGINS: str = "http://localhost http://localhost:9000"
    SLACK_ENDPOINT_URL: str = "http://test"
    BASE_URL: str = "http://localhost"
    DJANGO_SETTINGS_MODULE: str = "project.settings.local"


class AwsSettings(BaseSettings):
    """AWS関連の環境変数を設定するクラス"""

    AWS_SNS_ENDPOINT_URL: str = "http://localstack:4566"
    AWS_DEFAULT_REGION_NAME: str = "ap-northeast-1"
    AWS_SES_REGION_ENDPOINT: str = "email.ap-northeast-1.amazonaws.com"
    AWS_STORAGE_BUCKET_NAME: str = "localstack"
    SENDER: str = "example.co.jp"
    DEFAULT_FROM_EMAIL: str = "example.co.jp"


django_settings = DjangoSettings()


aws_settings = AwsSettings()
