import logging

from celery import shared_task
from .client import (S3, S3Error)

logger = logging.getLogger(__name__)


@shared_task
def s3copy(
    bucketname,
    src_keyname,
    dst_keyname
):
    s3 = S3().resource
    copy_source = {
        'Bucket': bucketname,
        'Key': src_keyname
    }
    try:
        s3.meta.client.copy(
            copy_source, bucketname, dst_keyname
        )
    except S3Error:
        # Thumbnails are not uploaded to S3 storage.
        # Thus, for every copy operation (for every page) there will
        # be one ClientError Exception because thumbnails
        # won't be found on S3
        pass
