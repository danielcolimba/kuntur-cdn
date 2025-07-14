# core/utils.py

import boto3
from botocore.client import Config
from django.conf import settings
import requests

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


def create_video_space(title): # Asign a title to the video space in bunny CDN
    url = f"https://video.bunnycdn.com/library/{settings.BUNNY_LIBRARY_ID}/videos"
    headers = {
        "AccessKey": settings.BUNNY_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {
        "title": title
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['guid']

def upload_video_bunny(video_id, file_path): # Upload the video file to Bunny CDN
    url = f"https://video.bunnycdn.com/library/{settings.BUNNY_LIBRARY_ID}/videos/{video_id}"
    headers = {
        "AccessKey": settings.BUNNY_API_KEY,
        "accept": "application/json"
    }
    with open(file_path, 'rb') as f:
        response = requests.put(url, headers=headers, data=f)
    response.raise_for_status()
    return True

def generate_url_bunny(video_id):
    # Bunny Stream genera URLs embebibles.
    return f"https://iframe.bunnycdn.com/embed/{video_id}"
