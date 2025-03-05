from datetime import date, datetime
from typing import Literal, TypedDict

import pytest


class AlbumTestModel(TypedDict):
    id: int
    title: str
    description: str | None
    picture_url: str | None
    type: Literal['single', 'album']
    created_at: date
    updated_at: datetime
    viewers_ids: list[int]
    likers_ids: list[int]
    artists_ids: list[int]
    tracks_ids: list[int]
    tags: list[str]


@pytest.fixture(scope="class")
def album() -> AlbumTestModel:
    return AlbumTestModel(
        id=1,
        title="title",
        description="description",
        picture_url="ftp://picture.png",
        type="single",
        created_at=date.today(),
        updated_at=datetime.now(),
        viewers_ids=[1],  # [user["id"]]
        likers_ids=[1],  # [user["id"]]
        artists_ids=[1],  # [artist["id"]]
        tracks_ids=[1],  # [track["id"]]
        tags=["tag"],
    )
