Cloud Storage
==============

This module enables Papermerge to store documents in the cloud (e.g. S3 cloud
storage),  this sort of "shared storage" for all papermerge instances (web and
workers).
It is used as part of Papermerge Cloud.

Installation
==============

Add cloud storage repository as dependency in requirements file::

    -e git+ssh://git@github.com/papermerge/cloud-storage.git#egg=cloud-storage


How to use it?
================

In papermerge.conf.py file set ``DEFAULT_FILE_STORAGE`` and ``FILE_STORAGE_KWARGS`` variables::

    DEFAULT_FILE_STORAGE = 'papermerge.storage.S3Storage'
    FILE_STORAGE_KWARGS = {
        'bucketname': 'dev_papermerge',
        'namespace': 'instance_id'
    }

Alternatively set ``PAPERMERGE_DEFAULT_FILE_STORAGE``  and ``PAPERMERGE_FILE_STORAGE_KWARGS`` in django settings file::

    PAPERMERGE_DEFAULT_FILE_STORAGE = 'papermerge.storage.S3Storage'
    PAPERMERGE_FILE_STORAGE_KWARGS = {
        'bucketname': 'bucket_name',
        'namespace': 'instance_id'
    }

Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY to enable papermerge upload/download files
to S3 bucket specified by ``bucket_name``::

    AWS_ACCESS_KEY_ID = 'your aws access key id'
    AWS_SECRET_ACCESS_KEY = 'your aws secret access key id'

both AWS_... variables need to be set either as part of django settings file
or as part of environment variables of respective process.
