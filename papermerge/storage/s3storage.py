import os
import logging
import boto3
from mglib.storage import FileSystemStorage


logger = logging.getLogger(__name__)


class S3Storage(FileSystemStorage):
    """
    Store documents on AWS S3 file system.
    Use local file system as first cache.
    """

    def __init__(self, bucketname, location=None):
        self._bucketname = bucketname
        super().__init__(location=location)

    @property
    def bucketname(self):
        return self._bucketname

    def upload(self, doc_path):

        local_url = self.abspath(doc_path.url())
        keyname = doc_path.url()
        s3_client = boto3.client('s3')

        if not os.path.exists(local_url):
            raise ValueError(f"{local_url} path does not exits")

        logger.debug(
            f"upload_document {local_url} to s3:/{self.bucketname}{keyname}"
        )

        s3_client.upload_file(
            local_url,
            self.bucketname,
            doc_path.url()
        )

    def download(self, doc_path):
        pass
