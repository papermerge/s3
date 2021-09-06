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
            "S3_SECRET_KEY", None
        )
        self._endpoint_url = os.environ.get(
            "S3_ENDPOINT_URL", None
        )
        self._client = boto3.client(
            's3',
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
            endpoint_url=self._endpoint_url
        )
        self._resource = boto3.resource(
            's3',
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
            endpoint_url=self._endpoint_url
        )

    @property
    def client(self):
        return self._client

    @property
    def resource(self):
        return self._resource
