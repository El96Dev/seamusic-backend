from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

from fastapi import UploadFile
from pydantic import EmailStr
from src.domain.music.albums.api.schemas import (
    BaseSUser,
    BaseSArtist,
    BaseSTrack,
    BaseSItemsRequest,
    BaseSAlbumRequest,
    BaseSAlbumResponse,
    BaseSAlbumItemResponse,
    BaseSPopularAlbumsResponse,
    BaseSCountAlbumsResponse,
    BaseSLikeAlbumRequest,
    BaseSUnlikeAlbumRequest,
    BaseSUpdateAlbumCoverRequest,
    BaseSCreateAlbumRequest,
    BaseSCreateAlbumResponse,
    BaseSUpdateAlbumRequest,
    BaseSUpdateAlbumResponse,
    BaseSDeleteAlbumRequest,
)


@dataclass
class SUser(BaseSUser):
    id: int
    username: str
    email: EmailStr
    password: str
    is_active: bool
    is_adult: bool
    is_verified: bool
    created_at: date
    updated_at: datetime
    access_level: Literal['user', 'admin', 'superuser'] = 'user'
    premium_level: Literal['none', 'bot', 'full'] = 'none'
    description: str | None = None
    picture_url: str | None = None
    telegram_id: int | None = None


@dataclass
class SArtist(BaseSArtist):
    id: int
    username: str
    user_id: int
    description: str | None = None
    picture_url: str | None = None


@dataclass
class STrack(BaseSTrack):
    id: int
    title: str
    file_url: str
    views: int
    likes: int
    created_at: date
    updated_at: datetime
    description: str | None = None
    picture_url: str | None = None


@dataclass
class SItemsRequest(BaseSItemsRequest):
    start: int = 1
    size: int = 10


@dataclass
class SAlbumRequest(BaseSAlbumRequest):
    album_id: int


@dataclass
class SAlbumResponse(BaseSAlbumResponse):
    id: int
    title: str
    type: Literal['album', 'single']
    views: int
    likes: int
    created_at: date
    updated_at: datetime
    artists: list[SArtist]
    tracks: list[STrack]
    tags: list[str]
    picture_url: str | None = None
    description: str | None = None


@dataclass
class SAlbumItemResponse(BaseSAlbumItemResponse):
    id: int
    title: str
    views: int
    likes: int
    type: Literal['album', 'single']
    created_at: date
    updated_at: datetime
    picture_url: str | None = None
    description: str | None = None


@dataclass
class SPopularAlbumsResponse(BaseSPopularAlbumsResponse):
    total: int
    page: int
    has_next: bool
    has_previous: bool
    size: int
    items: list[SAlbumItemResponse]


@dataclass
class SCountAlbumsResponse(BaseSCountAlbumsResponse):
    amount: int


@dataclass
class SLikeAlbumRequest(BaseSLikeAlbumRequest):
    album_id: int


@dataclass
class SUnlikeAlbumRequest(BaseSUnlikeAlbumRequest):
    album_id: int


@dataclass
class SUpdateAlbumCoverRequest(BaseSUpdateAlbumCoverRequest):
    album_id: int
    file: UploadFile


@dataclass
class SCreateAlbumRequest(BaseSCreateAlbumRequest):
    title: str
    tags: list[str]
    description: str | None = None


@dataclass
class SCreateAlbumResponse(BaseSCreateAlbumResponse):
    id: int


@dataclass
class SUpdateAlbumRequest(BaseSUpdateAlbumRequest):
    id: int
    title: str | None = None
    picture_url: str | None = None
    description: str | None = None
    artists_ids: list[int] | None = None
    tracks_ids: list[int] | None = None
    tags: list[str] | None = None


@dataclass
class SUpdateAlbumResponse(BaseSUpdateAlbumResponse):
    id: int


@dataclass
class SDeleteAlbumRequest(BaseSDeleteAlbumRequest):
    album_id: int
