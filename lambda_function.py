import uuid
import boto3 # type: ignore
from PIL import Image # type: ignore


s3_client = boto3.client('s3')


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image = image.resize((1024, 1024))  # Resize to 1024x1024 or any size you need
        image.save(resized_path, image.format)


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/resized-{}'.format(key)
        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)
        s3_client.upload_file(upload_path, bucket, 'resized/{}'.format(key))
