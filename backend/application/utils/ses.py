"""AWS関連のモジュール"""
from logging import getLogger

from application.utils.logs import LoggerName
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from injector import inject


class SESWrapper:
    """AWS SESのラッパークラス"""

    @inject
    def __init__(self, client: BaseClient):
        self.client = client

    def send_email(
        self,
        source: str,
        to_addresses: str,
        subject: str,
        body_text: str,
        charset: str,
    ) -> None:
        """AWS SESを用いてメールを送信

        Args:
            source (str): 送信元
            to_addresses (str): 送信先
            subject (str): メールの題名
            body_text (str): メールの本文
            charset(str): 文字コード
        """
        try:
            response = self.client.send_email(
                Destination={
                    "ToAddresses": [
                        to_addresses,
                    ],
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": charset,
                            "Data": body_text,
                        },
                    },
                    "Subject": {
                        "Charset": charset,
                        "Data": subject,
                    },
                },
                Source=source,
            )
        except ClientError as error:
            message = error.response["Error"]["Message"]
            getLogger(LoggerName.EMERGENCY.value).error(message)
        else:
            message = "Email sent! Message ID:", response["MessageId"]
            getLogger(LoggerName.APPLICATION.value).info(message)