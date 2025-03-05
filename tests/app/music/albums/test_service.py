from typing import Callable

import pytest

from src.app.music.albums.core.dtos import (
    AlbumResponseDTO,
    CreateAlbumResponseDTO,
    PopularAlbumsResponseDTO,
    UpdateAlbumResponseDTO,
)
from src.app.music.albums.core.service import get_service
from src.domain.music.albums.core.exceptions import AlbumNotFoundError
from src.domain.music.albums.core.service import BaseService
from src.infrastructure.exceptions import Exc
from tests.app.music.albums.fixtures import AlbumTestModel


@pytest.mark.album
@pytest.mark.album_service
class TestAlbumService:
    @pytest.fixture(scope="function")
    def service_factory(self) -> BaseService:
        return get_service()

    @pytest.fixture(scope="function")
    async def user_id(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def album_id(self, album: AlbumTestModel) -> int:
        return album["id"]

    @pytest.fixture(scope="function")
    def album_title(self, album: AlbumTestModel) -> str:
        return album["title"]

    @pytest.fixture(scope="function")
    def album_description(self, album: AlbumTestModel) -> str | None:
        return album["description"]

    @pytest.fixture(scope="function")
    def album_tags(self, album: AlbumTestModel) -> list[str]:
        return album["tags"]

    @pytest.fixture(scope="function")
    def album_artists_ids(self, album: AlbumTestModel) -> list[int]:
        return album["artists_ids"]

    @pytest.fixture(scope="function")
    def album_tracks_ids(self, album: AlbumTestModel) -> list[int]:
        return album["tracks_ids"]

    @pytest.fixture(scope="function")
    def album_cover_data(self) -> bytes:
        return bytes()

    @pytest.fixture(scope="function")
    def start(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def size(self) -> int:
        return 1

    async def test_create_album(  # TODO: add exceptions' parametrization
        self,
        service_factory: Callable[[], BaseService],
        user_id: int,
        album_title: str,
        album_description: str,
        album_tags: list[str],
        album: AlbumTestModel,
    ) -> None:
        response = await service_factory().create_album(
            title=album_title,
            user_id=user_id,
            description=album_description,
            tags=album_tags,
        )
        album["id"] = response.id
        assert isinstance(response.id, CreateAlbumResponseDTO)

    @pytest.mark.parametrize(
        "album_id,expected_type,expected_value,expected_exception",
        [
            (1, AlbumResponseDTO, None, None),  # TODO: add user_id parametrizaition
            (100, None, None, AlbumNotFoundError),
        ]
    )
    async def test_get_album(
        self,
        service_factory: Callable[[], BaseService],
        expected_type: type,
        expected_value: object,
        expected_exception: type[Exc],
        album_id: int,
        user_id: int,
    ) -> None:
        if expected_type:
            response = await service_factory().get_album(album_id=album_id, user_id=user_id)
            assert isinstance(response, expected_type)
        if expected_value:
            response = await service_factory().get_album(album_id=album_id, user_id=user_id)
            assert response == expected_value
        if expected_exception:
            with pytest.raises(expected_exception):
                await service_factory().get_album(album_id=album_id, user_id=user_id)

    async def test_get_popular_albums(
        self,
        service_factory: Callable[[], BaseService],
        user_id: int,
        start: int,
        size: int,
    ) -> None:
        response = await service_factory().get_popular_albums(
            user_id=user_id,
            start=start,
            size=size,
        )
        assert isinstance(response, PopularAlbumsResponseDTO)

    @pytest.mark.parametrize(
        "album_id",
        [(1,), (100,)]
    )
    async def test_like_album(  # TODO: add user_id parametrizaition after authentication is done
        self,
        service_factory: Callable[[], BaseService],
        album_id: int,
        user_id: int,
    ) -> None:
        if album_id == 1:
            assert await service_factory().like_album(album_id=album_id, user_id=user_id) is None  # type: ignore[func-returns-value]
        else:
            with pytest.raises(AlbumNotFoundError):
                await service_factory().like_album(album_id=album_id, user_id=user_id)

    @pytest.mark.parametrize(
        "album_id",
        [(1,), (100,)]
    )
    async def test_unlike_album(  # TODO: add user_id parametrizaition after authentication is done
        self,
        service_factory: Callable[[], BaseService],
        album_id: int,
        user_id: int,
    ) -> None:
        if album_id == 1:
            assert await service_factory().unlike_album(album_id=album_id, user_id=user_id) is None  # type: ignore[func-returns-value]
        else:
            with pytest.raises(AlbumNotFoundError):
                await service_factory().unlike_album(album_id=album_id, user_id=user_id)

    @pytest.mark.parametrize(  # TODO: add user_id parametrizaition after authentication is done
        "album_id,expected_type,expected_value,expected_exception",
        [
            (1, CreateAlbumResponseDTO, None, None),
            (100, None, None, AlbumNotFoundError),
        ]
    )
    async def test_update_album(
        self,
        service_factory: Callable[[], BaseService],
        expected_type: type,
        expected_value: object,
        expected_exception: type[Exc],
        album_id: int,
        album_title: str,
        album_description: str,
        album_artists_ids: list[int],
        album_tracks_ids: list[int],
        album_tags: list[str],
        user_id: int,
        album: AlbumTestModel,
    ) -> None:
        if expected_type:
            response = await service_factory().update_album(
                album_id=album_id,
                user_id=user_id,
                title=album_title,
                description=album_description,
                artists_ids=album_artists_ids,
                tracks_ids=album_tracks_ids,
                tags=album_tags,
            )
            assert isinstance(response, UpdateAlbumResponseDTO)
            album["id"] = response.id
        if expected_value:
            response = await service_factory().update_album(
                album_id=album_id,
                user_id=user_id,
                title=album_title,
                description=album_description,
                artists_ids=album_artists_ids,
                tracks_ids=album_tracks_ids,
                tags=album_tags,
            )
            assert response == expected_value
        if expected_exception:
            with pytest.raises(expected_exception):
                await service_factory().update_album(
                    album_id=album_id,
                    user_id=user_id,
                    title=album_title,
                    description=album_description,
                    artists_ids=album_artists_ids,
                    tracks_ids=album_tracks_ids,
                    tags=album_tags,
                )

    @pytest.mark.parametrize(
        "album_id",
        [(1,), (100,)]
    )
    async def test_update_cover(
        self,
        service_factory: Callable[[], BaseService],
        album_id: int,
        album_cover_data: bytes,
        user_id: int
    ) -> None:
        if album_id == 1:
            assert await service_factory().update_cover(  # type: ignore[func-returns-value]
                user_id=user_id,
                album_id=album_id,
                data=album_cover_data,
            ) is None
        else:
            with pytest.raises(AlbumNotFoundError):
                await service_factory().update_cover(
                    user_id=user_id,
                    album_id=album_id,
                    data=album_cover_data,
                )

    async def test_delete_album(
        self,
        service_factory: BaseService,
        album_id: int,
        user_id: int,
    ) -> None:
        assert await service_factory.delete_album(album_id=album_id, user_id=user_id) is None  # type: ignore[func-returns-value]
        with pytest.raises(AlbumNotFoundError):
            await service_factory.get_album(album_id=album_id, user_id=user_id)
