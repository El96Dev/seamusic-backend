import os
from io import BytesIO
from types import TracebackType
from typing import Self
from uuid import uuid4

from boto3 import Session as Boto3Session, client as boto3client

from src.infrastructure.config import settings


class S3SessionMixin(Boto3Session):
    """
    S3SessionMixin is a mixin class for media interface implementation
    that is designed to use Yandex Cloud S3 storage there and should
    only be used via its subclass' asynchronous context manager
    """

    def __init__(self) -> None:
        super().__init__(
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        self.client: boto3client = self.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net')
        self.bucket_name: str = settings.bucket_name

    async def read(self, path: str, filename: str) -> str:
        return os.path.join('https://storage.yandexcloud.net/', self.bucket_name, path, filename)

    async def write(self, path: str, filename: str, file_stream: BytesIO) -> str:
        key = os.path.join(path, filename)
        self.client.upload_fileobj(file_stream, self.bucket_name, key)
        file_url = os.path.join('https://storage.yandexcloud.net/', self.bucket_name, key)
        return file_url

    async def update(self, path: str, filename: str, file_stream: BytesIO) -> str:
        key = os.path.join(path, filename)
        self.client.upload_fileobj(file_stream, self.bucket_name, key)
        file_url = os.path.join('https://storage.yandexcloud.net/', self.bucket_name, key)
        return file_url

    async def remove(self, path: str, filename: str) -> None:
        key = f'{path}/{filename}'
        self.client.delete_object(Bucket=self.bucket_name, Key=key)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[Exception] | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass


def unique_filename(filename: str) -> str:
    file_name, file_extension = os.path.splitext(filename)
    return f'{file_name.replace(" ", "-")}_{uuid4()}{file_extension}'


def get_file_stream(data: bytes) -> BytesIO:
    # await file.read()
    return BytesIO(data)
