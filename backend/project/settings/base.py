"""
Django settings for application project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from logging.config import dictConfig
from pathlib import Path

from application.utils.logs import ConfFile

from .environment import django_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECRET_KEYを.envから取得
SECRET_KEY = django_settings.SECRET_KEY

# ALLOWED_HOSTSを.envから取得
ALLOWED_HOSTS = django_settings.ALLOWED_HOSTS.split()

# Application definition

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ]
}


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "application.apps.ApplicationConfig",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "application.utils.middleware.LoggingMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # コンテナ内の環境変数をDATABASESのパラメータに反映
        "NAME": django_settings.POSTGRES_NAME,
        "USER": django_settings.POSTGRES_USER,
        "PASSWORD": django_settings.POSTGRES_PASSWORD,
        "HOST": django_settings.POSTGRES_HOST,
        "PORT": django_settings.POSTGRES_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "application.User"

# STATIC_ROOTを設定
STATIC_ROOT = "/static/"
STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/upload/"
MEDIA_ROOT = os.path.join(BASE_DIR, "upload")

# 自身以外のオリジンのHTTPリクエスト内にクッキーを含めることを許可する
CORS_ALLOW_CREDENTIALS = True
# アクセスを許可したいURL（アクセス元）を追加
CORS_ALLOWED_ORIGINS = django_settings.TRUSTED_ORIGINS.split()
# プリフライト(事前リクエスト)の設定
# 30分だけ許可
CORS_PREFLIGHT_MAX_AGE = 60 * 30

# ログ設定
dictConfig(ConfFile.get()["logging"])
