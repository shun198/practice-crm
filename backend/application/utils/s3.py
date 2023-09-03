from logging import Logger, getLogger

from botocore.exceptions import ClientError
from injector import inject
from storages.backends.s3boto3 import S3Boto3Storage

from application.utils.logs import LoggerName
from project.settings.environment import aws_settings

application_logger: Logger = getLogger(LoggerName.APPLICATION.value)
emergency_logger: Logger = getLogger(LoggerName.EMERGENCY.value)


class S3BucketResource:
    """S3のResource用のクラス"""

    def __init__(self, bucket):
        self.bucket = bucket
        self.name = bucket


class S3BucketWrapper:
    """Encapsulates S3 bucket actions."""

    @inject
    def __init__(self, bucket: S3Boto3Storage):
        """
        :param bucket: A Boto3 Bucket resource. This is a high-level resource in Boto3
                       that wraps bucket actions in a class-like structure.
        """
        self.bucket = bucket
        self.name = bucket

    def create(self, region_override=None):
        """
        Create an Amazon S3 bucket in the default Region for the account or in the
        specified Region.

        :param region_override: The Region in which to create the bucket. If this is
                                not specified, the Region configured in your shared
                                credentials is used.
        """
        region = aws_settings.AWS_DEFAULT_REGION_NAME
        try:
            self.bucket.create(
                CreateBucketConfiguration={"LocationConstraint": region}
            )

            self.bucket.wait_until_exists()
            application_logger.info(
                "Created bucket '%s' in region=%s", self.bucket.name, region
            )
        except ClientError as error:
            emergency_logger.exception(
                "Couldn't create bucket named '%s' in region=%s.",
                self.bucket.name,
                region,
            )
            raise error
