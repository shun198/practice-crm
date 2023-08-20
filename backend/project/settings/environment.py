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


class AwsSettings(BaseSettings):
    """AWS関連の環境変数を設定するクラス"""

    ENDPOINT_URL: str = "http://localstack:4566"
    AWS_DEFAULT_REGION_NAME: str = "ap-northeast-1"
    AWS_STORAGE_BUCKET_NAME: str = "localstack"
    SENDER: str = "example.co.jp"


django_settings = DjangoSettings()


aws_settings = AwsSettings()
