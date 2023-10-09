import json
import tomllib
from enum import Enum
from logging import getLogger
from typing import Any, Optional

import requests
from django.utils.log import AdminEmailHandler

from project.settings.environment import django_settings


class LoggerName(Enum):
    """ロガー名"""

    APPLICATION = "application"
    EMERGENCY = "emergency"


class ConfFile:
    """confファイル取得用クラス
    Attributes:
        _conf_file (Optional[dict[Any, Any]]): pyproject.tomlのデータを辞書形式に変換した内容<br>
            最初の1回だけ読み込まれる
    """

    _conf_file: Optional[dict[Any, Any]] = None

    @classmethod
    def get(cls) -> dict[Any, Any]:
        """pyproject.tomlのデータを辞書形式で返す
        2回目以降はファイルの読み込みは実施しない
        Returns:
            dict[Any, Any]: pyproject.tomlの設定データの辞書形式
        """
        if cls._conf_file is None:
            with open("pyproject.toml", mode="rb") as file:
                cls._conf_file = tomllib.load(file)
        return cls._conf_file


class SlackHandler(AdminEmailHandler):
    def send_mail(self, subject, message, *args, **kwargs):
        webhook_url = django_settings.SLACK_ENDPOINT_URL
        if "Request" in message:
            alarm_emoji = ":rotating_light:"
            text = alarm_emoji + message.split("COOKIES")[0]
            data = json.dumps(
                {
                    "attachments": [{"color": "#e01d5a", "text": text}],
                }
            )
            headers = {"Content-Type": "application/json"}
            getLogger(LoggerName.EMERGENCY.value).error(message)
            requests.post(url=webhook_url, data=data, headers=headers)
