# core/utils.py

import boto3
from botocore.client import Config
from django.conf import settings

def upload_video_to_b2(file_path, object_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        config=Config(signature_version='s3v4')
    )
    s3.upload_file(file_path, settings.AWS_STORAGE_BUCKET_NAME, object_name)
    return f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{object_name}"
