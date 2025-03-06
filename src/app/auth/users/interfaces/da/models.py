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

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    description: Mapped[str | None]
    email: Mapped[str]
    password: Mapped[str]
    picture_url: Mapped[str | None]

    created_at: Mapped[date]
    updated_at: Mapped[datetime]

    access_level: Mapped[str]
    premium_level: Mapped[str]
    telegram_id: Mapped[int | None]
    is_verified: Mapped[bool]

    artist_id: Mapped[int] = mapped_column(ForeignKey("artist_profiles.id"))
    producer_id: Mapped[int] = mapped_column(ForeignKey("producer_profiles.id"))

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
    licenses: Mapped[list[License]] = relationship(
        argument="License",
        secondary=author_to_licenses_association,
        back_populates="author",
        lazy="selectin",
    )
    followed_squads: Mapped[list[Squad]] = relationship(
        argument="Squad",
        secondary=follower_to_squads_association,
        back_populates="followers",
        lazy="selectin",
    )
    followed_artists: Mapped[list[ArtistProfile]] = relationship(
        argument="ArtistProfile",
        secondary=followers_to_artists_association,
        back_populates="followers",
        lazy="selectin",
    )
    coauthored_playlists: Mapped[list[Playlist]] = relationship(
        argument="Playlist",
        secondary=author_to_playlists_association,
        back_populates="authors",
        lazy="selectin",
    )
    saved_playlists: Mapped[list[Playlist]] = relationship(
        argument="Playlist",
        secondary=saver_to_playlists_association,
        lazy="selectin",
    )
    followed_producers: Mapped[list[ProducerProfile]] = relationship(
        argument="ProducerProfile",
        secondary=followers_to_producers_association,
        back_populates="followers",
        lazy="selectin",
    )
    saved_albums: Mapped[list[Album]] = relationship(
        argument="Album",
        secondary=saver_to_albums_association,
        lazy="selectin",
    )
    followed_tags: Mapped[list[Tag]] = relationship(
        argument="Tag",
        secondary=follower_to_tag_association,
        lazy="selectin",
    )
