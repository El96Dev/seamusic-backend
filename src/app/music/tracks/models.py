from datetime import datetime, date

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.app.auth.artists.models import ArtistProfile, artists_to_tracks_association
from src.infrastructure.postgres import Base, IntArray

track_to_tag_association = Table(
    "track_to_tag_association",
    Base.metadata,
    Column("track_id", ForeignKey("tracks.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

track_to_producer_association = Table(
    "track_to_producer_association",
    Base.metadata,
    Column("producer_id", ForeignKey("producer_profiles.id"), primary_key=True),
    Column("track_id", ForeignKey("tracks.id"), primary_key=True),
)

user_to_tracks_likes = Table(
    "user_to_tracks_likes",
    Base.metadata,
    Column("track_id", ForeignKey("tracks.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True)
)


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str | None]
    picture_url: Mapped[str | None]
    file_url: Mapped[str]

    viewers_ids: Mapped[IntArray]
    likers_ids: Mapped[IntArray]

    created_at: Mapped[date]
    updated_at: Mapped[datetime]

    artists: Mapped[list["ArtistProfile"]] = relationship(
        argument="ArtistProfile",
        secondary=artists_to_tracks_association,
        back_populates="tracks",
        lazy="selectin",
    )
    producers: Mapped[list["ProducerProfile"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="ProducerProfile",
        secondary=track_to_producer_association,
        lazy="selectin",
    )
    tags: Mapped[list["Tag"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Tag",
        secondary=track_to_tag_association,
        lazy="selectin",
    )
