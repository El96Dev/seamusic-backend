from datetime import date, datetime
from typing import Literal, Callable

import pytest

from src.app.music.albums.interfaces.da.dao import PostgresDAOImplementation, get_postgres_dao_implementation
from src.app.music.albums.interfaces.da.models import Album
from src.app.music.albums.interfaces.ma.mao import S3MAOImplementation, get_s3_mao_implementation
from tests.app.music.albums.fixtures import AlbumTestModel, album  # noqa: F401


@pytest.mark.album
@pytest.mark.album_dao
class TestPostgresDAOImplementation:
    @pytest.fixture(scope="function")
    def dao_impl_factory(self) -> Callable[[], PostgresDAOImplementation]:
        return get_postgres_dao_implementation

    @pytest.fixture(scope="function")
    def album_id(self, album: AlbumTestModel) -> int:
        return album['id']

    @pytest.fixture(scope="function")
    def album_title(self, album: AlbumTestModel) -> str:
        return album["title"]

    @pytest.fixture(scope="function")
    def album_type(self, album: AlbumTestModel) -> Literal["album", "single"]:
        return album["type"]

    @pytest.fixture(scope="function")
    def album_created_at(self, album: AlbumTestModel) -> date:
        return album["created_at"]

    @pytest.fixture(scope="function")
    def album_updated_at(self, album: AlbumTestModel) -> datetime:
        return album["updated_at"]

    @pytest.fixture(scope="function")
    def album_viewers_ids(self, album: AlbumTestModel) -> list[int]:
        return album["viewers_ids"]

    @pytest.fixture(scope="function")
    def album_likers_ids(self, album: AlbumTestModel) -> list[int]:
        return album["likers_ids"]

    @pytest.fixture(scope="function")
    def album_artists_ids(self, album: AlbumTestModel) -> list[int]:
        return album["artists_ids"]

    @pytest.fixture(scope="function")
    def album_tracks_ids(self, album: AlbumTestModel) -> list[int]:
        return album["tracks_ids"]

    @pytest.fixture(scope="function")
    def album_tags(self, album: AlbumTestModel) -> list[str]:
        return album["tags"]

    @pytest.fixture(scope="function")
    def artist_id(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def album_picture_url(self, album: AlbumTestModel) -> str | None:
        return album["picture_url"]

    @pytest.fixture(scope="function")
    def album_description(self, album: AlbumTestModel) -> str | None:
        return album["description"]

    @pytest.fixture(scope="function")
    def start(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def size(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def user_id(self, album: AlbumTestModel) -> int:
        return 1

    async def test_create_album(
        self,
        album_title: str,
        album_description: str | None,
        album_picture_url: str | None,
        album_type: Literal["album", "single"],
        album_created_at: date,
        album_updated_at: datetime,
        album_viewers_ids: list[int],
        album_likers_ids: list[int],
        album_artists_ids: list[int],
        album_tracks_ids: list[int],
        album_tags: list[str],
        dao_impl_factory: Callable[[], PostgresDAOImplementation],
        album: AlbumTestModel,
    ) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.create_album(
                title=album_title,
                album_type=album_type,
                created_at=album_created_at,
                updated_at=album_updated_at,
                viewers_ids=album_viewers_ids,
                likers_ids=album_likers_ids,
                artists_ids=album_artists_ids,
                tracks_ids=album_tracks_ids,
                tags=album_tags,
                picture_url=album_picture_url,
                description=album_description,
            )
        assert isinstance(response, int)
        assert response >= 1
        album["id"] = response

    async def test_get_album_by_id(
        self,
        album_id: int,
        dao_impl_factory: Callable[[], PostgresDAOImplementation],
    ) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_album_by_id(album_id=album_id)
        assert isinstance(response, Album)

        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_album_by_id(album_id=100)
        assert response is None

    async def test_get_album_existance_by_title(
        self,
        artist_id: int,
        album_title: str,
        dao_impl_factory: Callable[[], PostgresDAOImplementation],
    ) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_album_existance_by_title(artist_id=artist_id, title=album_title)
        assert isinstance(response, bool)

    async def test_get_album_existance_by_id(self, album: AlbumTestModel, dao_impl_factory: Callable[[], PostgresDAOImplementation]) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_album_existance_by_id(album_id=album["id"])
        assert isinstance(response, bool)

    async def test_get_popular_albums(self, start: int, size: int, dao_impl_factory: Callable[[], PostgresDAOImplementation]) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_popular_albums(start=start, size=size)
        assert isinstance(response, list)

    async def test_count_albums(self, dao_impl_factory: Callable[[], PostgresDAOImplementation]) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.count_albums()
        assert isinstance(response, int)
        assert response >= 0

    async def test_get_artist_id_by_user_id(self, user_id: int, dao_impl_factory: Callable[[], PostgresDAOImplementation]) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_artist_id_by_user_id(user_id=user_id)
        assert isinstance(response, int)
        assert response >= 1

    async def test_update_album(
        self,
        album: AlbumTestModel,
        dao_impl_factory: Callable[[], PostgresDAOImplementation],
        album_id: int,
        album_title: str | None,
        album_picture_url: str | None,
        album_description: str | None,
        album_type: Literal["album", "single"] | None,
        album_created_at: date | None,
        album_updated_at: datetime | None,
        album_viewers_ids: list[int] | None,
        album_likers_ids: list[int] | None,
        album_artists_ids: list[int] | None,
        album_tracks_ids: list[int] | None,
        album_tags: list[str] | None,
    ) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.update_album(
                album_id=album_id,
                title=album_title,
                picture_url=album_picture_url,
                description=album_description,
                album_type=album_type,
                created_at=album_created_at,
                updated_at=album_updated_at,
                viewers_ids=album_viewers_ids,
                likers_ids=album_likers_ids,
                artists_ids=album_artists_ids,
                tracks_ids=album_tracks_ids,
                tags=album_tags,
            )
        assert isinstance(response, int)
        assert response >= 1
        album["id"] = response

    async def test_delete_album(self, album: AlbumTestModel, dao_impl_factory: Callable[[], PostgresDAOImplementation]) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.delete_album(album_id=album["id"])  # type: ignore[func-returns-value]
        assert response is None


@pytest.mark.album
@pytest.mark.album_dao
class TestS3MAOImplementation:
    @pytest.fixture(scope="function")
    def mao_impl_factory(self) -> Callable[[], S3MAOImplementation]:
        return get_s3_mao_implementation

    @pytest.fixture(scope="function")
    def data(self) -> bytes:
        return bytes()

    @pytest.fixture(scope="function")
    def album_id(self) -> int:
        return 1

    async def test_update_cover(self, data: bytes, album_id: int, mao_impl_factory: Callable[[], S3MAOImplementation]) -> None:
        async with mao_impl_factory() as mao_impl:
            response = await mao_impl.update_cover(album_id=album_id, data=data)
        assert isinstance(response, str)
