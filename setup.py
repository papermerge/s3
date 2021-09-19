from setuptools import setup, find_namespace_packages

setup(
    packages=find_namespace_packages(include=['papermerge.*']),
    install_requires=[
        "mglib == 1.3.9",
        "boto3 == 1.18.36",
        "botocore == 1.21.36",
        "celery == 5.0.5"
    ]
)
