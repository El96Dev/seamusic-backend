from abc import ABC
from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, Any, Sequence


@dataclass
class BaseCurrentUser(ABC):
    id: int


@dataclass
class BaseSUser(ABC):
    id: int
    username: str
    email: str
    password: str
    is_active: bool
    is_adult: bool
    is_verified: bool
    created_at: date
    updated_at: datetime
    picture_url: str | None = None
    description: str | None = None
    telegram_id: int | None = None
    access_level: Literal['user', 'admin', 'superuser'] = 'user'
    premium_level: Literal['none', 'bot', 'full'] = 'none'


@dataclass
class BaseSArtist(ABC):
    id: int
    username: str
    user_id: int
    description: str | None = None
    picture_url: str | None = None


@dataclass
class BaseSTrack(ABC):
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
class BaseSItemsRequest(ABC):
    start: int = 1
    size: int = 10


@dataclass
class BaseSAlbumRequest(ABC):
    album_id: int


@dataclass
class BaseSAlbumResponse(ABC):
    id: int
    title: str
    type: Literal['album', 'single']
    views: int
    likes: int
    created_at: date
    updated_at: datetime
    artists: Sequence[BaseSArtist]
    tracks: Sequence[BaseSTrack]
    tags: Sequence[str]
    picture_url: str | None = None
    description: str | None = None


@dataclass
class BaseSAlbumItemResponse(ABC):
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
class BaseSPopularAlbumsResponse(ABC):
    total: int
    page: int
    has_next: bool
    has_previous: bool
    size: int
    items: Sequence[BaseSAlbumItemResponse]


@dataclass
class BaseSCountAlbumsResponse(ABC):
    amount: int


@dataclass
class BaseSArtistAlbumsRequest(ABC):
    artist_id: int


@dataclass
class BaseSArtistAlbumsResponse(ABC):
    total: int
    items: Sequence[BaseSAlbumItemResponse]


@dataclass
class BaseSLikeAlbumRequest(ABC):
    album_id: int


@dataclass
class BaseSUnlikeAlbumRequest(ABC):
    album_id: int


@dataclass
class BaseSUpdateAlbumCoverRequest(ABC):
    album_id: int
    file: Any


@dataclass
class BaseSCreateAlbumRequest(ABC):
    title: str
    tags: Sequence[str]
    description: str | None = None


@dataclass
class BaseSCreateAlbumResponse(ABC):
    id: int


@dataclass
class BaseSUpdateAlbumRequest(ABC):
    id: int
    title: str | None = None
    picture_url: str | None = None
    description: str | None = None
    artists_ids: Sequence[int] | None = None
    tracks_ids: Sequence[int] | None = None
    tags: Sequence[str] | None = None


@dataclass
class BaseSUpdateAlbumResponse(ABC):
    id: int


@dataclass
class BaseSDeleteAlbumRequest(ABC):
    album_id: int
