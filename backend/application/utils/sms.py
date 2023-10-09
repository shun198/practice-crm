from logging import Logger, getLogger

from botocore.exceptions import ClientError
from injector import inject

from application.utils.logs import LoggerName

application_logger: Logger = getLogger(LoggerName.APPLICATION.value)
emergency_logger: Logger = getLogger(LoggerName.EMERGENCY.value)


# https://docs.aws.amazon.com/ja_jp/sns/latest/dg/example_sns_PublishTextSMS_section.html
class SnsResource:
    """SNSのResource用のクラス"""

    def __init__(self, sns_resource):
        self.sns_resource = sns_resource


class SnsWrapper:
    """Encapsulates Amazon SNS topic and subscription functions."""

    # オブジェクト注入する際に@injectデコレータを使用
    @inject
    def __init__(self, sns_resource: SnsResource):
        """
        :param sns_resource: A Boto3 Amazon SNS resource.
        """
        self.sns_resource = sns_resource.sns_resource

    def publish_text_message(self, phone_number, message):
        """
        Publishes a text message directly to a phone number without need for a
        subscription.

        :param phone_number: The phone number that receives the message. This must be
                            in E.164 format. For example, a United States phone
                            number might be +12065550101.
        :param message: The message to send.
        :return: The ID of the message.
        """
        try:
            response = self.sns_resource.meta.client.publish(
                PhoneNumber=phone_number, Message=message
            )
            message_id = response["MessageId"]
            application_logger.info("Published message to %s.", phone_number)
        except ClientError:
            emergency_logger.exception(
                "Couldn't publish message to %s.", phone_number
            )
            raise
        else:
            return message_id
