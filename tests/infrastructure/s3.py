import os
from io import BytesIO
from typing import BinaryIO

import pytest

from src.infrastructure.s3 import S3SessionMixin, unique_filename, get_file_stream


class TestS3SessionMixin:
    @pytest.fixture(scope="function")
    def mixin(self) -> S3SessionMixin:
        return S3SessionMixin()

    @pytest.fixture(scope="function")
    def filename(self) -> str:
        return "filename"

    @pytest.fixture(scope="function")
    def path(self) -> str:
        return "/path/"

    @pytest.fixture(scope="function")
    def file_stream(self) -> BytesIO:
        return BytesIO()

    async def test_read(self, path: str, filename: str, mixin: S3SessionMixin) -> None:
        async with mixin as session:
            response = await session.read(path, filename)
        assert isinstance(response, str)
        assert response.startswith("https://storage.yandexcloud.net/")
        assert response.endswith(os.path.join(path, filename))

    async def test_write(self, path: str, filename: str, file_stream: BytesIO, mixin: S3SessionMixin) -> None:
        async with mixin as session:
            response = await session.write(path, filename, file_stream)
        assert isinstance(response, str)

    async def test_update(self, path: str, filename: str, file_stream: BytesIO, mixin: S3SessionMixin) -> None:
        async with mixin as session:
            response = await session.update(path, filename, file_stream)
        assert isinstance(response, str)

    async def test_remove(self, path: str, filename: str, mixin: S3SessionMixin) -> None:
        async with mixin as session:
            await session.remove(path, filename)


class TestFileActions:
    @pytest.fixture(scope="function")
    def filename(self) -> str:
        return "filename"

    @pytest.fixture(scope="function")
    def data(self) -> bytes:
        return bytes()

    def test_unique_filename(self, filename: str) -> None:
        response = unique_filename(filename)
        assert isinstance(response, str)

    def test_get_file_stream(self, data: bytes) -> None:
        response = get_file_stream(data)
        assert isinstance(response, BinaryIO)
