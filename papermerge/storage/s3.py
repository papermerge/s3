import boto3
import botocore


class S3Error(botocore.exceptions.ClientError):
    pass


class S3:

    def __init__(self):
        self._client = boto3.client('s3')
        self._resource = boto3.resource('s3')

    @property
    def client(self):
        return self._client

    @property
    def resource(self):
        return self._resource
