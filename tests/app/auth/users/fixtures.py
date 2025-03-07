from datetime import date, datetime
from typing import Literal, TypedDict

import pytest

AccessLevel = Literal["user", "admin", "superuser"]
PremiumLevel = Literal["none", "bot", "full"]


class UserTestModel(TypedDict):
    id: int
    username: str
    description: str | None
    email: str
    password: str
    picture_url: str | None
    created_at: date
    updated_at: datetime
    telegram_id: int | None
    access_level: AccessLevel
    premium_level: PremiumLevel
    is_verified: bool
    artist_id: int
    producer_id: int
    licenses_ids: list[int]
    followed_squads_ids: list[int]
    followed_artists_ids: list[int]
    coauthored_playlists_ids: list[int]
    saved_playlists_ids: list[int]
    followed_producers_ids: list[int]
    saved_albums_ids: list[int]
    followed_tags: list[str]


@pytest.fixture(scope="session")
def user() -> UserTestModel:
    return UserTestModel(
        id=1,
        username="username",
        description="description",
        email="user@example.com",
        password="qwerty1234",
        picture_url="ftp://picture.png",
        created_at=date.today(),
        updated_at=datetime.now(),
        telegram_id=None,
        access_level="user",
        premium_level="none",
        is_verified=True,
        artist_id=1,
        producer_id=1,
        licenses_ids=[1],
        followed_squads_ids=[1],
        followed_artists_ids=[1],
        coauthored_playlists_ids=[1],
        saved_playlists_ids=[1],
        followed_producers_ids=[1],
        saved_albums_ids=[1],
        followed_tags=["tag"],
    )
