from datetime import date, datetime

from sqlalchemy import Table, ForeignKey, Integer, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.app.auth.producers.models import ProducerProfile, user_to_producer_association, followers_to_producers_association
from src.app.music.squads.models import Squad, follower_to_squads_association
from src.app.social.playlists.models import Playlist, author_to_playlists_association
from src.app.social.tags.models import Tag
from src.infrastructure.postgres import Base

author_to_licenses_association = Table(
    "author_to_licenses_association",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("license_id", Integer, ForeignKey("licenses.id"), primary_key=True),
)

user_to_artist_association = Table(
    "user_to_artist_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("artist_id", Integer, ForeignKey("artist_profiles.id"), primary_key=True),
)

followers_to_artists_association = Table(
    "followers_to_artists_association",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("artist_id", Integer, ForeignKey("artist_profiles.id"), primary_key=True),
)

saver_to_albums_association = Table(
    "saver_to_albums_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("album_id", Integer, ForeignKey("albums.id"), primary_key=True),
)

follower_to_tag_association = Table(
    "follower   _to_tag_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

saver_to_playlists_association = Table(
    "saver_to_playlists_association",
    Base.metadata,
    Column("saver_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    description: Mapped[str | None]
    email: Mapped[str]
    password: Mapped[str]
    picture_url: Mapped[str | None]
    access_level: Mapped[str]
    telegram_id: Mapped[int | None]
    premium_level: Mapped[str]

    created_at: Mapped[date]
    updated_at: Mapped[datetime]

    is_active: Mapped[bool]
    is_adult: Mapped[bool]
    is_verified: Mapped[bool]

    artist_id: Mapped[int] = mapped_column(ForeignKey("artist_profiles.id"))
    producer_id: Mapped[int] = mapped_column(ForeignKey("producer_profiles.id"))

    artist_profile: Mapped["ArtistProfile"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="ArtistProfile",
        secondary=user_to_artist_association,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    producer_profile: Mapped["ProducerProfile"] = relationship(
        argument="ProducerProfile",
        secondary=user_to_producer_association,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    licenses: Mapped[list["License"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="License",
        secondary=author_to_licenses_association,
        lazy="selectin",
    )
    followed_squads: Mapped[list["Squad"]] = relationship(
        argument="Squad",
        secondary=follower_to_squads_association,
        back_populates="followers",
        lazy="selectin",
    )
    followed_artists: Mapped[list["ArtistProfile"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="ArtistProfile",
        secondary=followers_to_artists_association,
        back_populates="users",
        lazy="selectin",
    )
    coauthored_playlists: Mapped[list["Playlist"]] = relationship(
        argument="Playlist",
        secondary=author_to_playlists_association,
        back_populates="authors",
        lazy="selectin",
    )
    saved_playlists: Mapped[list["Playlist"]] = relationship(
        argument="Playlist",
        secondary=saver_to_playlists_association,
        lazy="selectin",
    )
    followed_producers: Mapped[list["ProducerProfile"]] = relationship(
        argument="ProducerProfile",
        secondary=followers_to_producers_association,
        lazy="selectin",
    )
    saved_albums: Mapped[list["Album"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Album",
        secondary=saver_to_albums_association,
        lazy="selectin",
    )
    followed_tags: Mapped[list["Tag"]] = relationship(
        argument="Tag",
        secondary=follower_to_tag_association,
        lazy="selectin",
    )
