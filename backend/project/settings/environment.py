"""環境変数定義用のモジュール"""

from pydantic import BaseSettings


class DjangoSettings(BaseSettings):
    """Django関連の環境変数を設定するクラス"""

    SECRET_KEY: str = "secretkey"
    ALLOWED_HOSTS: str = "localhost 127.0.0.1 [::1] back web"
    MYSQL_DATABASE: str = "django-db"
    MYSQL_USER: str = "django"
    MYSQL_PASSWORD: str = "django"
    MYSQL_HOST: str = "db"
    MYSQL_PORT: int = 3306
    TRUSTED_ORIGINS: str = "http://localhost"


class AwsSettings(BaseSettings):
    """AWS関連の環境変数を設定するクラス"""

    ENDPOINT_URL: str = "http://localstack:4566"
    AWS_DEFAULT_REGION_NAME: str = "ap-northeast-1"
    AWS_STORAGE_BUCKET_NAME: str = "localstack"
    DEFAULT_FROM_EMAIL: str = "example@gmail.com"
    AWS_PROFILE: str = "localstack"


django_settings = DjangoSettings()


aws_settings = AwsSettings()
