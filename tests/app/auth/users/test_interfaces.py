from datetime import date, datetime
from typing import Literal, Callable

import pytest

from src.app.auth.users.interfaces.da.dao import PostgresDAOImplementation, get_postgres_dao_implementation
from src.app.auth.users.interfaces.da.models import User
from src.app.auth.users.interfaces.ma.mao import S3MAOImplementation, get_s3_mao_implementation
from tests.app.auth.users.fixtures import UserTestModel, AccessLevel, PremiumLevel, user  # noqa: F401


@pytest.mark.user
@pytest.mark.user_dao
class TestPostgresDAOImplementation:
    @pytest.fixture(scope="function")
    def dao_impl_factory(self) -> Callable[[], PostgresDAOImplementation]:
        return get_postgres_dao_implementation

    @pytest.fixture(scope="function")
    def user_id(self, user: UserTestModel) -> int:
        return user["id"]

    @pytest.fixture(scope="function")
    def username(self, user: UserTestModel) -> str:
        return user["username"]

    @pytest.fixture(scope="function")
    def description(self, user: UserTestModel) -> str | None:
        return user["description"]

    @pytest.fixture(scope="function")
    def email(self, user: UserTestModel) -> str:
        return user["email"]

    @pytest.fixture(scope="function")
    def password(self, user: UserTestModel) -> str:
        return user["password"]

    @pytest.fixture(scope="function")
    def picture_url(self, user: UserTestModel) -> str | None:
        return user["picture_url"]

    @pytest.fixture(scope="function")
    def created_at(self, user: UserTestModel) -> date:
        return user["created_at"]

    @pytest.fixture(scope="function")
    def updated_at(self, user: UserTestModel) -> datetime:
        return user["updated_at"]

    @pytest.fixture(scope="function")
    def telegram_id(self, user: UserTestModel) -> int | None:
        return user["telegram_id"]

    @pytest.fixture(scope="function")
    def access_level(self, user: UserTestModel) -> AccessLevel:
        return user["access_level"]

    @pytest.fixture(scope="function")
    def premium_level(self, user: UserTestModel) -> PremiumLevel:
        return user["premium_level"]

    @pytest.fixture(scope="function")
    def is_verified(self, user: UserTestModel) -> bool:
        return user["is_verified"]

    @pytest.fixture(scope="function")
    def artist_id(self, user: UserTestModel) -> int:
        return user["artist_id"]

    @pytest.fixture(scope="function")
    def producer_id(self, user: UserTestModel) -> int:
        return user["producer_id"]

    @pytest.fixture(scope="function")
    def licenses_ids(self, user: UserTestModel) -> list[int]:
        return user["licenses_ids"]

    @pytest.fixture(scope="function")
    def followed_squads_ids(self, user: UserTestModel) -> list[int]:
        return user["followed_squads_ids"]

    @pytest.fixture(scope="function")
    def followed_artists_ids(self, user: UserTestModel) -> list[int]:
        return user["followed_artists_ids"]

    @pytest.fixture(scope="function")
    def coauthored_playlists_ids(self, user: UserTestModel) -> list[int]:
        return user["coauthored_playlists_ids"]

    @pytest.fixture(scope="function")
    def saved_playlists_ids(self, user: UserTestModel) -> list[int]:
        return user["saved_playlists_ids"]

    @pytest.fixture(scope="function")
    def followed_producers_ids(self, user: UserTestModel) -> list[int]:
        return user["followed_producers_ids"]

    @pytest.fixture(scope="function")
    def saved_albums_ids(self, user: UserTestModel) -> list[int]:
        return user["saved_albums_ids"]

    @pytest.fixture(scope="function")
    def followed_tags(self, user: UserTestModel) -> list[str]:
        return user["followed_tags"]

    @pytest.fixture(scope="function")
    def start(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def size(self) -> int:
        return 1

    async def test_get_user_by_id(self, user_id: int, dao_impl_factory: Callable[[], PostgresDAOImplementation]) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_user_by_id(user_id=user_id)
        assert isinstance(response, User)

        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_user_by_id(user_id=100)
        assert response is None

    async def test_get_user_by_username(self, username: str, dao_impl_factory: Callable[[], PostgresDAOImplementation]) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_user_by_username(username=username)
        assert isinstance(response, User)

        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_user_by_username(username=username)
        assert response is None

    async def test_get_users(self, dao_impl_factory: Callable[[], PostgresDAOImplementation]) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.get_users()
        assert isinstance(response, list)

    async def test_count_users(self, dao_impl_factory: Callable[[], PostgresDAOImplementation]) -> None:
        async with dao_impl_factory() as dao_impl:
            response = dao_impl.count_users()
        assert isinstance(response, int)

    async def test_create_user(
        self,
        email: str,
        password: str,
        username: str,
        created_at: date,
        updated_at: datetime,
        access_level: Literal["user", "admin", "superuser"],
        premium_level: Literal["none", "bot", "full"],
        is_verified: bool,
        artist_id: int,
        producer_id: int,
        licenses_ids: list[int],
        followed_squads_ids: list[int],
        followed_artists_ids: list[int],
        coauthored_playlists_ids: list[int],
        saved_playlists_ids: list[int],
        followed_producers_ids: list[int],
        saved_albums_ids: list[int],
        followed_tags: list[str],
        telegram_id: int | None,
        description: str | None,
        picture_url: str | None,
        dao_impl_factory: Callable[[], PostgresDAOImplementation],
    ) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.create_user(
                email=email,
                password=password,
                username=username,
                created_at=created_at,
                updated_at=updated_at,
                access_level=access_level,
                premium_level=premium_level,
                is_verified=is_verified,
                artist_id=artist_id,
                producer_id=producer_id,
                licenses_ids=licenses_ids,
                followed_squads_ids=followed_squads_ids,
                followed_artists_ids=followed_artists_ids,
                coauthored_playlists_ids=coauthored_playlists_ids,
                saved_playlists_ids=saved_playlists_ids,
                followed_producers_ids=followed_producers_ids,
                saved_albums_ids=saved_albums_ids,
                followed_tags=followed_tags,
                telegram_id=telegram_id,
                description=description,
                picture_url=picture_url,
            )
        assert isinstance(response, int)

    async def test_update_user(
        self,
        user_id: int,
        username: str | None,
        description: str | None,
        email: str | None,
        password: str | None,
        picture_url: str | None,
        created_at: date | None,
        updated_at: datetime | None,
        access_level: AccessLevel | None,
        premium_level: PremiumLevel | None,
        artist_id: int | None,
        producer_id: int | None,
        telegram_id: int | None,
        is_verified: bool | None,
        licenses_ids: list[int] | None,
        followed_squads_ids: list[int] | None,
        followed_artists_ids: list[int] | None,
        coauthored_playlists_ids: list[int] | None,
        saved_playlists_ids: list[int] | None,
        followed_producers_ids: list[int] | None,
        saved_albums_ids: list[int] | None,
        followed_tags: list[str] | None,
        dao_impl_factory: Callable[[], PostgresDAOImplementation],
    ) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.update_user(
                user_id=user_id,
                username=username,
                description=description,
                email=email,
                password=password,
                picture_url=picture_url,
                created_at=created_at,
                updated_at=updated_at,
                access_level=access_level,
                premium_level=premium_level,
                artist_id=artist_id,
                producer_id=producer_id,
                telegram_id=telegram_id,
                is_verified=is_verified,
                licenses_ids=licenses_ids,
                followed_squads_ids=followed_squads_ids,
                followed_artists_ids=followed_artists_ids,
                coauthored_playlists_ids=coauthored_playlists_ids,
                saved_playlists_ids=saved_playlists_ids,
                followed_producers_ids=followed_producers_ids,
                saved_albums_ids=saved_albums_ids,
                followed_tags=followed_tags,
            )
        assert isinstance(response, int)

    async def test_delete_user(self, user_id: int, dao_impl_factory: Callable[[], PostgresDAOImplementation]) -> None:
        async with dao_impl_factory() as dao_impl:
            response = await dao_impl.delete_user(user_id=user_id)  # type: ignore[func-returns-value]
        assert response is None


@pytest.mark.user
@pytest.mark.user_dao
class TestS3MAOImplementation:
    @pytest.fixture(scope="function")
    def mao_impl_factory(self) -> Callable[[], S3MAOImplementation]:
        return get_s3_mao_implementation

    @pytest.fixture(scope="function")
    def data(self) -> bytes:
        return bytes()

    @pytest.fixture(scope="function")
    def user_id(self, user: UserTestModel) -> int:
        return user["id"]

    async def test_update_cover(self, data: bytes, user_id: int, mao_impl_factory: Callable[[], S3MAOImplementation]) -> None:
        async with mao_impl_factory() as mao_impl:
            response = await mao_impl.update_profile_picture(user_id=user_id, data=data)
        assert isinstance(response, str)
