import tomllib
from enum import Enum
from typing import Any, Optional


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
