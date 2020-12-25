import boto3
import botocore
import logging

from celery import shared_task


logger = logging.getLogger(__name__)


@shared_task
def s3copy(
    bucketname,
    src_keyname,
    dst_keyname
):
    s3 = boto3.resource('s3')
    copy_source = {
        'Bucket': bucketname,
        'Key': src_keyname
    }
    try:
        s3.meta.client.copy(
            copy_source, bucketname, dst_keyname
        )
    except botocore.exceptions.ClientError:
        # Thumbnails are not uploaded to S3 storage.
        # Thus, for every copy operation (for every page) there will
        # be one ClientError Exception because thumbnails
        # won't be found on S3
        pass
