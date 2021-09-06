import os
import boto3
import botocore


class S3Error(botocore.exceptions.ClientError):
    pass


class S3:

    def __init__(self):
        self._aws_access_key_id = os.environ.get(
            "S3_ACCESS_KEY_ID", None
        )
        self._aws_secret_access_key = os.environ.get(
            "S3_SECRET_ACCESS_KEY", None
        )
        self._endpoint_url = os.environ.get(
            "S3_ENDPOINT_URL", None
        )
        self._region_name = os.environ.get(
            "S3_REGION_NAME",
            None
        )
        self._session = boto3.Session(
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
            region_name=self._region_name
        )
        self._client = self._session.client(
            's3',
            endpoint_url=self._endpoint_url
        )

    @property
    def client(self):
        return self._client
