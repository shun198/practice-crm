"""LOCAL環境用の設定"""
import boto3

from .base import *
from .environment import aws_settings

DEBUG = True

REST_FRAMEWORK.update(
    {"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"}
)

SPECTACULAR_SETTINGS = {
    "TITLE": "プロジェクト名",
    "DESCRIPTION": "詳細",
    "VERSION": "1.0.0",
}

INSTALLED_APPS += [
    "debug_toolbar",
    "drf_spectacular",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]


DEBUG_TOOLBAR_CONFIG = {
    # ツールバーを表示させる
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

ROOT_URLCONF = "project.urls.local"

# Djangoのメールの設定
EMAIL_HOST = "mail"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
# SMTPの1025番ポートを指定
EMAIL_PORT = 1025
# 送信中の文章の暗号化をFalseにします
EMAIL_USE_TLS = False

CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]

# メールの設定
EMAIL_HOST = "mail"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_USE_TLS = False

# Create an SNS client
SNS_CLIENT = boto3.client(
    "sns",
    aws_access_key_id="localstack",
    aws_secret_access_key="localstack",
    region_name=aws_settings.AWS_DEFAULT_REGION_NAME,
    endpoint_url=aws_settings.AWS_SNS_ENDPOINT_URL,
)
