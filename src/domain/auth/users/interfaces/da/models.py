from datetime import date, datetime
from typing import Literal


class BaseUserModel:
    id: int
    username: str
    description: str | None
    email: str
    password: str
    picture_url: str | None

    created_at: date
    updated_at: datetime

    telegram_id: int | None
    access_level: Literal["user", "admin", "superuser"]
    premium_level: Literal["none", "bot", "full"]
    is_verified: bool

    artist_id: int
    producer_id: int

    artist_profile: "BaseArtistProfileModel"  # type: ignore[name-defined]  # noqa: F821
    producer_profile: "BaseProducerProfileModel"  # type: ignore[name-defined]  # noqa: F821
    licenses: list["BaseLicenseModel"]  # type: ignore[name-defined]  # noqa: F821
    followed_squads: list["BaseSquadModel"]  # type: ignore[name-defined]  # noqa: F821
    followed_artists: list["BaseArtistProfileModel"]  # type: ignore[name-defined]  # noqa: F821
    coauthored_playlists: list["BasePlaylistModel"]  # type: ignore[name-defined]  # noqa: F821
    saved_playlists: list["BasePlaylistModel"]  # type: ignore[name-defined]  # noqa: F821
    followed_producers: list["BaseProducerProfileModel"]  # type: ignore[name-defined]  # noqa: F821
    saved_albums: list["BaseAlbumModel"]  # type: ignore[name-defined]  # noqa: F821
    followed_tags: list["BaseTagModel"]  # type: ignore[name-defined]  # noqa: F821
