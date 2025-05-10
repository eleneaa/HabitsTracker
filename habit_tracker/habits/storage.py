import boto3
from django.conf import settings


def upload_to_yandex_storage(file, filename):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=settings.YC_ACCESS_KEY,
        aws_secret_access_key=settings.YC_SECRET_KEY
    )

    s3.upload_fileobj(file, settings.YC_BUCKET_NAME, filename)
    return f"https://{settings.YC_BUCKET_NAME}.storage.yandexcloud.net/{filename}"