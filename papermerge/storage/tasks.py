import logging

from celery import shared_task
from .s3 import (S3, S3Error)

logger = logging.getLogger(__name__)


@shared_task
def s3copy(
    bucketname,
    src_keyname,
    dst_keyname
):
    s3_instance = S3()
    s3_client = s3_instance.client
    try:
        s3_client.upload_file(
            src_keyname,
            bucketname,
            dst_keyname
        )
    except S3Error:
        # Thumbnails are not uploaded to S3 storage.
        # Thus, for every copy operation (for every page) there will
        # be one ClientError Exception because thumbnails
        # won't be found on S3
        pass
