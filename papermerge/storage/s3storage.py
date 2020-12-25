import os
import logging
import boto3
import botocore

from mglib.storage import FileSystemStorage


logger = logging.getLogger(__name__)


class S3Storage(FileSystemStorage):
    """
    Store documents on AWS S3 file system.
    Use local file system as first cache.

    Configuration for S3Storage:

    # replace default storage with this one
    DEFAULT_FILE_STORAGE = "papermerge.storage.S3Storage"

    # pass bucketname and namespace keys
    PAPERMERGE_FILE_STORAGE_KWARGS = {
        'bucketname': 'dev_papermerge',
        'namespace': 'dev_eugen'
    }

    Whay we need ``namespace`` argument?

    The thing is we use one bucket name for multiple papermerge
    tenants/instances. Each instance uses completely different data. Thus, if
    in each instance, user id=1 creates document id=3 their documents will
    overlap bucket/user_1/document_1/...
    To differenciate between two instances - namespace is introduced.

    Example of paths to the document X.pdf:

        s3://bucketname/namespace/docs/user_3/document_23/X.pdf
        s3://bucketname/namespace/docs/user_3/document_23/v1/X.pdf
    """

    def __init__(self, location=None, **kwargs):
        """
        ``location`` is ``mglib.path.DocumentPath`` instance

        kwargs['bucketname'] is AWS S3 bucket name
        kwargs['namespace'] is sort of tenant name e.g. name of the
        instance deployed
        """
        self._bucketname = kwargs.pop('bucketname', None)
        self._namespace = kwargs.pop('namespace', None)

        if not self._bucketname:
            raise ValueError("bucketname argument is empty")

        if not self._namespace:
            raise ValueError("namespace argument is empty")

        super().__init__(location=location, **kwargs)

    @property
    def namespace(self):
        return self._namespace

    @property
    def bucketname(self):
        return self._bucketname

    def upload(self, doc_path, **kwargs):
        """
        kwargs['namespace'] if provided, will be used instead of
        local self._namespace.
        Why ?
        Workers run for all papermerge instances, thus they need
        to be instructed about namespace.
        """
        local_url = self.abspath(doc_path.url())
        # prefix doc_path with self._namespace

        # kwarg['namespace'] overrides local namespace
        namespace = kwargs.get('namespace', self._namespace)
        keyname = os.path.join(namespace, doc_path.url())
        s3_client = boto3.client('s3')

        if not os.path.exists(local_url):
            raise ValueError(f"{local_url} path does not exits")

        logger.debug(
            f"upload_document {local_url} to s3:/{self.bucketname}{keyname}"
        )

        s3_client.upload_file(
            local_url,
            self.bucketname,
            keyname
        )

    def download(self, doc_path, **kwargs):
        local_url = self.abspath(doc_path)
        namespace = kwargs.get('namespace', self._namespace)
        keyname = os.path.join(namespace, doc_path.url())

        s3_client = boto3.client('s3')

        if not os.path.exists(local_url):
            logger.debug(f"{local_url} does not exists. Creating.")
            os.makedirs(
                local_url, exist_ok=True
            )
        else:
            logger.debug(f"{local_url} already exists.")

        keyname = os.path.join(namespace, doc_path.url())

        try:
            s3_client.download_file(
                self.bucketname,
                keyname,
                local_url
            )
        except botocore.exceptions.ClientError:
            logger.error(
                f"Error while downloading "
                f" {self.bucketname}/{keyname} to {local_url}",
                exc_info=True
            )
            return False

