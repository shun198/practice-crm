"""AWS関連のモジュール"""
from logging import Logger, getLogger

from botocore.exceptions import ClientError
from injector import inject

from application.utils.logs import LoggerName

application_logger: Logger = getLogger(LoggerName.APPLICATION.value)
emergency_logger: Logger = getLogger(LoggerName.EMERGENCY.value)


class SesResource:
    """SesのResource用のクラス"""

    def __init__(self, ses_resource):
        self.ses_resource = ses_resource


class SesWrapper:
    """Encapsulates Amazon SES topic and subscription functions."""

    @inject
    def __init__(self, sns_resource: SesResource):
        """
        :param sns_resource: A Boto3 Amazon SNS resource.
        """
        self.sns_resource = sns_resource.sns_resource

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
            emergency_logger.exception(message)
        else:
            message = "Email sent! Message ID:", response["MessageId"]
            emergency_logger.exception(message)
