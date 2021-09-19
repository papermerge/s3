# S3 Storage

This module enables Papermerge to store documents in S3 object storage.

## Installation

Add cloud storage repository as dependency in requirements file:

    pip install papermerge-s3

## How to use it?

In papermerge.conf.py file set ``DEFAULT_FILE_STORAGE`` and

``FILE_STORAGE_KWARGS`` variables:

    DEFAULT_FILE_STORAGE = 'papermerge.storage.S3Storage'
    FILE_STORAGE_KWARGS = {
        'bucketname': '<bucketname>',
        'namespace': '<namespace>'
    }

Alternatively set ``PAPERMERGE_DEFAULT_FILE_STORAGE``  and
``PAPERMERGE_FILE_STORAGE_KWARGS`` in django settings file:

    PAPERMERGE_DEFAULT_FILE_STORAGE = 'papermerge.storage.S3Storage'
    PAPERMERGE_FILE_STORAGE_KWARGS = {
        'bucketname': '<bucketname>',
        'namespace': '<namespace>'
    }

Set following evironment variables:

    S3_ACCESS_KEY_ID = 'your aws access key id'
    S3_SECRET_ACCESS_KEY = 'your aws secret access key id'
    S3_ENDPOINT_URL = '<endpoint url>'
    S3_REGION_NAME = '<region name>'
