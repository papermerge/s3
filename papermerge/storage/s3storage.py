import os
import logging

from mglib.storage import FileSystemStorage
from mglib.path import DocumentPath

from .s3 import (
    S3,
    S3Error
)
from .tasks import s3copy


logger = logging.getLogger(__name__)


class S3Storage(FileSystemStorage):
    """
    Store documents on S3 file system.
    Use local file system as first cache.

    Configuration for S3:

    # replace default storage with this one
    DEFAULT_FILE_STORAGE = "papermerge.storage.S3Storage"

    # pass bucketname and namespace keys
    PAPERMERGE_FILE_STORAGE_KWARGS = {
        'bucketname': 'backetname',
        'namespace': 'namespace'
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

        Bucketname must always be supplied.
        Namespace will be supplied in case s3storage runs as part
        of web app.
        In case of worker deployment context namepace will be None
        in __init__. In case of workers, namepace must be provided
        in download/upload functions. It is so because workers
        are shared between tenants, thus only at upload/download
        stage it is know for which tenant that work is performed.
        """
        self._bucketname = kwargs.pop('bucketname', None)
        # For web app ``namespace`` != None
        # For worker ``namespace`` is None
        self._namespace = kwargs.pop('namespace', None)

        if not self._bucketname:
            raise ValueError("bucketname argument is empty")

        super().__init__(location=location, **kwargs)

    @property
    def namespace(self):
        return self._namespace

    @property
    def bucketname(self):
        return self._bucketname

    def upload(self, doc_path_url, **kwargs):
        """
        doc_path_url: str - is relative to media root path to
        file to upload
        kwargs['namespace'] if provided, will be used instead of
        local self._namespace.
        Why ?
        Workers run for all papermerge instances, thus they need
        to be instructed about namespace.

        On successful upload returns namespace as string.
        (in main app code returned namespace is passed to async task)
        """
        local_url = self.abspath(doc_path_url)
        # prefix doc_path with self._namespace

        # kwarg['namespace'] overrides local namespace
        namespace = kwargs.get('namespace', self._namespace)
        keyname = os.path.join(namespace, doc_path_url)
        s3_client = S3().client

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

        return self.namespace

    def download(self, doc_path_url, **kwargs):
        local_url = self.abspath(doc_path_url)
        namespace = kwargs.get('namespace', self._namespace)

        if not namespace:
            logger.error(
                f"Namespace empty for {doc_path_url}"
            )
            return

        keyname = os.path.join(namespace, doc_path_url)

        s3_client = S3().client

        self.make_sure_path_exists(
            filepath=self.abspath(doc_path_url)
        )

        keyname = os.path.join(namespace, doc_path_url)

        try:
            s3_client.download_file(
                Bucket=self.bucketname,
                Key=keyname,
                Filename=local_url
            )
        except S3Error:
            logger.error(
                f"Error while downloading "
                f" {self.bucketname}/{keyname} to {local_url}",
                exc_info=True
            )
            return

    def copy_page_hocr(self, src_page_path, dst_page_path):

        abs_path = self.abspath(src_page_path.hocr_url())
        if not os.path.exists(abs_path):
            self.download(src_page_path.hocr_url())

        super().copy_page_hocr(src_page_path, dst_page_path)
        self._s3copy(
            src=src_page_path.hocr_url(),
            dst=dst_page_path.hocr_url()
        )

    def copy_page_txt(self, src_page_path, dst_page_path):

        abs_path = self.abspath(src_page_path.txt_url())
        if not os.path.exists(abs_path):
            self.download(src_page_path.txt_url())

        super().copy_page_txt(src_page_path, dst_page_path)
        self._s3copy(
            src=src_page_path.txt_url(),
            dst=dst_page_path.txt_url()
        )

    def copy_page_img(self, src_page_path, dst_page_path):
        abs_path = self.abspath(src_page_path.img_url())
        if not os.path.exists(abs_path):
            self.download(src_page_path.img_url())

        super().copy_page_img(src_page_path, dst_page_path)
        self._s3copy(
            src=src_page_path.img_url(),
            dst=dst_page_path.img_url()
        )

    def copy_doc(self, src, dst):
        super().copy_doc(
            src=src,
            dst=dst
        )
        if isinstance(src, DocumentPath):
            self._s3copy(
                src=src.url(),
                dst=dst.url()
            )
        else:
            self._s3copy(src=src, dst=dst)

    def _s3copy(self, src, dst):

        src_keyname = os.path.join(
            self.namespace, src
        )
        dst_keyname = os.path.join(
            self.namespace, dst
        )
        s3copy(
            bucketname=self.bucketname,
            src_keyname=src_keyname,
            dst_keyname=dst_keyname
        )
