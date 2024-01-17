"""DEV環境用の設定"""
import boto3

from .base import *
from .environment import aws_settings

DEBUG = False
ROOT_URLCONF = "project.urls.base"

INSTALLED_APPS += [
    "django_ses",
    "storages",
]


# SESの設定
EMAIL_BACKEND = "django_ses.SESBackend"
AWS_DEFAULT_REGION_NAME = aws_settings.AWS_DEFAULT_REGION_NAME
AWS_SES_REGION_ENDPOINT = aws_settings.AWS_SES_REGION_ENDPOINT
DEFAULT_FROM_EMAIL = aws_settings.DEFAULT_FROM_EMAIL
# S3の設定
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
AWS_STORAGE_BUCKET_NAME = aws_settings.AWS_STORAGE_BUCKET_NAME

# Create an SNS client
SNS_CLIENT = boto3.client(
    "sns",
    region_name=aws_settings.AWS_DEFAULT_REGION_NAME,
    endpoint_url=aws_settings.AWS_SNS_ENDPOINT_URL,
)
