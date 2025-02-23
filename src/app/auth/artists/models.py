from datetime import date, datetime

from sqlalchemy import Table, Integer, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.auth.users.models import followers_to_artists_association
from src.app.music.albums.interfaces.da.models import album_to_artist_association
from src.app.music.squads.models import artist_to_squad_association
from src.infrastructure.postgres import Base

artists_to_tracks_association = Table(
    "artists_to_track_association",
    Base.metadata,
    Column("artist_profile_id", Integer, ForeignKey("artist_profiles.id"), primary_key=True),
    Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True),
)

artists_to_tags_association = Table(
    "artists_to_tags_association",
    Base.metadata,
    Column("artist_id", ForeignKey("artist_profiles.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class ArtistProfile(Base):
    __tablename__ = "artist_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    description: Mapped[str | None]
    picture_url: Mapped[str | None]

    created_at: Mapped[date]
    updated_at: Mapped[datetime]
    is_available: Mapped[bool]

    followers: Mapped[list["User"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="User",
        secondary=followers_to_artists_association,
        back_populates="followed_artists",
        lazy="selectin",
    )
    tracks: Mapped[list["Track"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Track",
        secondary=artists_to_tracks_association,
        back_populates="artists",
        lazy="selectin",
    )
    squads: Mapped[list["Squad"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Squad",
        secondary=artist_to_squad_association,
        lazy="selectin",
    )
    albums: Mapped[list["Album"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Album",
        secondary=album_to_artist_association,
        lazy="selectin",
    )
    tags: Mapped[list["Tag"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Tag",
        secondary=artists_to_tags_association,
        lazy="selectin",
    )
