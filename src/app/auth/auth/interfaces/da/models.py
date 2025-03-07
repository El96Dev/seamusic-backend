from datetime import date, datetime

from sqlalchemy import Table, ForeignKey, Integer, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.app.auth.artists.models import user_to_artist_association, ArtistProfile, followers_to_artists_association
from src.app.auth.producers.models import (
    ProducerProfile,
    user_to_producer_association,
    followers_to_producers_association,
)
from src.app.music.albums.interfaces.da.models import saver_to_albums_association, Album
from src.app.music.squads.models import Squad, follower_to_squads_association
from src.app.social.licenses.models import author_to_licenses_association, License
from src.app.social.playlists.models import Playlist, author_to_playlists_association
from src.app.social.tags.models import Tag
from src.domain.auth.users.interfaces.da.models import BaseUserModel
from src.infrastructure.postgres import Base

follower_to_tag_association = Table(
    "follower_to_tag_association",
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


class User(BaseUserModel, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # type: ignore[assignment]
    username: Mapped[str]  # type: ignore[assignment]
    description: Mapped[str | None]  # type: ignore[assignment]
    email: Mapped[str]  # type: ignore[assignment]
    password: Mapped[str]  # type: ignore[assignment]
    picture_url: Mapped[str | None]  # type: ignore[assignment]

    created_at: Mapped[date]  # type: ignore[assignment]
    updated_at: Mapped[datetime]  # type: ignore[assignment]

    access_level: Mapped[str]  # type: ignore[assignment]
    premium_level: Mapped[str]  # type: ignore[assignment]
    telegram_id: Mapped[int | None]  # type: ignore[assignment]
    is_verified: Mapped[bool]  # type: ignore[assignment]

    artist_id: Mapped[int] = mapped_column(ForeignKey("artist_profiles.id"))  # type: ignore[assignment]
    producer_id: Mapped[int] = mapped_column(ForeignKey("producer_profiles.id"))  # type: ignore[assignment]

    artist_profile: Mapped[ArtistProfile] = relationship(
        argument="ArtistProfile",
        secondary=user_to_artist_association,
        cascade="all, delete-orphan",
        single_parent=True,
        lazy="joined",
    )
    producer_profile: Mapped[ProducerProfile] = relationship(
        argument="ProducerProfile",
        secondary=user_to_producer_association,
        cascade="all, delete-orphan",
        single_parent=True,
        lazy="joined",
    )
    licenses: Mapped[list[License]] = relationship(  # type: ignore[assignment]
        argument="License",
        secondary=author_to_licenses_association,
        back_populates="author",
        lazy="selectin",
    )
    followed_squads: Mapped[list[Squad]] = relationship(  # type: ignore[assignment]
        argument="Squad",
        secondary=follower_to_squads_association,
        back_populates="followers",
        lazy="selectin",
    )
    followed_artists: Mapped[list[ArtistProfile]] = relationship(  # type: ignore[assignment]
        argument="ArtistProfile",
        secondary=followers_to_artists_association,
        back_populates="followers",
        lazy="selectin",
    )
    coauthored_playlists: Mapped[list[Playlist]] = relationship(  # type: ignore[assignment]
        argument="Playlist",
        secondary=author_to_playlists_association,
        back_populates="authors",
        lazy="selectin",
    )
    saved_playlists: Mapped[list[Playlist]] = relationship(  # type: ignore[assignment]
        argument="Playlist",
        secondary=saver_to_playlists_association,
        lazy="selectin",
    )
    followed_producers: Mapped[list[ProducerProfile]] = relationship(  # type: ignore[assignment]
        argument="ProducerProfile",
        secondary=followers_to_producers_association,
        back_populates="followers",
        lazy="selectin",
    )
    saved_albums: Mapped[list[Album]] = relationship(  # type: ignore[assignment]
        argument="Album",
        secondary=saver_to_albums_association,
        lazy="selectin",
    )
    followed_tags: Mapped[list[Tag]] = relationship(  # type: ignore[assignment]
        argument="Tag",
        secondary=follower_to_tag_association,
        lazy="selectin",
    )
