"""DEV環境用の設定"""

from application.injectors.s3 import DevS3Module, s3_injector
from application.injectors.ses import DevSesModule, ses_injector
from application.injectors.sns import DevSnsModule, sns_injector

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
DEFAULT_FROM_EMAIL = aws_settings.DEFAULT_FROM_EMAIL
# S3の設定
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
AWS_STORAGE_BUCKET_NAME = aws_settings.AWS_STORAGE_BUCKET_NAME

# DI設定
sns_injector.binder.install(DevSnsModule())
s3_injector.binder.install(DevS3Module())
ses_injector.binder.install(DevSesModule())
