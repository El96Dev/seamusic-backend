import pytest

from src.app.music.albums.core.dtos import AlbumResponseDTO, ArtistAlbumsResponseDTO
from src.app.music.albums.core.service import get_service
from src.domain.music.albums.core.exceptions import AlbumNotFoundError
from src.domain.music.albums.core.service import BaseService
from typing import TypedDict


class AlbumTestModel(TypedDict):
    """
        TypedDict class for check types
    """
    album_id: int | None
    album_title: str
    album_description: str
    album_tags: list[str]
    artists_ids: list[int]
    tracks_ids: list[int]


class TestAlbumService:
    """
    Fixtures
    """

    @pytest.fixture(scope='session')
    def album_service_factory(self) -> BaseService:
        return get_service()

    @pytest.fixture(scope='session')
    def fixture_album_title(self) -> str:
        return 'title'

    @pytest.fixture(scope='session')
    def fixture_album_description(self) -> str:
        return 'description'

    @pytest.fixture(scope='session')
    def fixture_album_tags(self) -> list[str]:
        return ['one tag', 'two tag']

    @pytest.fixture(scope='session')
    def fixture_artists_ids(self) -> list[int]:
        return []

    @pytest.fixture(scope='session')
    def fixture_tracks_ids(self) -> list[int]:
        return []

    @pytest.fixture(scope='session')
    def fixture_artist_id(self) -> int:
        return 1

    @pytest.fixture(scope='session')
    def fixture_album_dict(
            self,
            fixture_album_title: str,
            fixture_album_description: str,
            fixture_album_tags,
            fixture_artists_ids,
            fixture_tracks_ids
    ) -> dict:
        return {
            'album_id': None,
            'title': fixture_album_title,
            'description': fixture_album_description,
            'tags': fixture_album_tags,
            'artists_ids': fixture_artists_ids,
            'tracks_ids': fixture_tracks_ids
        }

    """
        Testing functions
    """

    async def test_create_album(
            self,
            album_service_factory: BaseService,
            user_id: int,
            fixture_album_title: str,
            fixture_album_description: str,
            fixture_album_tags: list[str],
            fixture_album_dict: AlbumTestModel
    ):
        result_create_album = await album_service_factory.create_album(
            title=fixture_album_title,
            description=fixture_album_description,
            tags=fixture_album_tags,
            user_id=user_id
        )
        assert isinstance(result_create_album.id, int) and result_create_album.id >= 1
        fixture_album_dict['album_id'] = result_create_album.id

    async def test_get_album_by_id(
            self,
            album_service_factory: BaseService,
            fixture_album_dict: AlbumTestModel,
            user_id: int
    ):
        result_get_album = await album_service_factory.get_album(album_id=fixture_album_dict['album_id'],
                                                                 user_id=user_id)
        assert isinstance(result_get_album, AlbumResponseDTO) and result_get_album.id == fixture_album_dict['album_id']

    async def test_exist_viewer_in_albums(
            self,
            album_service_factory: BaseService,
            fixture_album_dict: AlbumTestModel,
            user_id: int
    ):
        result_get_album = await album_service_factory.get_album(album_id=fixture_album_dict['album_id'],
                                                                 user_id=user_id)
        assert result_get_album.views == 1

    async def test_update_album(
            self,
            album_service_factory: BaseService,
            user_id: int,
            fixture_album_title: str,
            fixture_album_description: str,
            fixture_album_tags: list[str],
            fixture_artists_ids: list[int],
            fixture_tracks_ids: list[int],
            fixture_album_dict: AlbumTestModel
    ):
        result_update_album = await album_service_factory.update_album(
            album_id=fixture_album_dict["album_id"],
            user_id=user_id,
            title=fixture_album_title,
            description=fixture_album_description,
            tags=fixture_album_tags,
            artists_ids=fixture_artists_ids,
            tracks_ids=fixture_tracks_ids
        )
        assert isinstance(result_update_album.id, int) and result_update_album.id >= 1

    async def test_like_album(
            self,
            album_service_factory: BaseService,
            fixture_album_dict: AlbumTestModel,
            user_id: int,
    ):
        await album_service_factory.like_album(album_id=fixture_album_dict['album_id'], user_id=user_id)
        result_album_by_id = await album_service_factory.get_album(album_id=fixture_album_dict['album_id'],
                                                                   user_id=user_id)
        assert result_album_by_id.likes == 1

    async def test_unlike_album(
            self,
            album_service_factory: BaseService,
            fixture_album_dict: AlbumTestModel,
            user_id: int,
    ):
        await album_service_factory.unlike_album(album_id=fixture_album_dict['album_id'], user_id=user_id)
        result_album_by_id = await album_service_factory.get_album(album_id=fixture_album_dict['album_id'],
                                                                   user_id=user_id)
        assert result_album_by_id.likes == 0

    async def test_get_artists_albums(
            self,
            album_service_factory: BaseService,
            artists_id: int
    ):
        result_album_by_artist_id = await album_service_factory.get_artists_albums(artist_id=artists_id)
        assert result_album_by_artist_id.total >= 1

    async def test_get_popular_albums(
            self,
            album_service_factory: BaseService,
            fixture_album_dict: AlbumTestModel,
            user_id: int,
    ):
        result_popular_albums = await album_service_factory.get_popular_albums(
            user_id=user_id, start=0, size=10
        )
        assert result_popular_albums.total >= 1

    async def test_delete_album(
            self,
            album_service_factory: BaseService,
            fixture_album_dict: AlbumTestModel,
            user_id: int
    ):
        try:
            await album_service_factory.delete_album(user_id=user_id, album_id=fixture_album_dict["album_id"])
            await album_service_factory.get_album(album_id=fixture_album_dict['album_id'], user_id=user_id)
            assert False
        except AlbumNotFoundError:
            assert True
