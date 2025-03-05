from datetime import date, datetime

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.infrastructure.postgres import Base, IntArray

playlists_to_beat_association = Table(
    "playlists_to_beat_association",
    Base.metadata,
    Column("playlists_id", ForeignKey("playlists.id"), primary_key=True),
    Column("beat_id", ForeignKey("beats.id"), primary_key=True),
)

playlists_to_track_association = Table(
    "playlists_to_track_association",
    Base.metadata,
    Column("playlists_id", ForeignKey("playlists.id"), primary_key=True),
    Column("track_id", ForeignKey("tracks.id"), primary_key=True),
)

playlists_to_tag_association = Table(
    "playlists_to_tag_association",
    Base.metadata,
    Column("playlists_id", ForeignKey("playlists.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

author_to_playlists_association = Table(
    "user_to_playlists_author_association",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlists.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class Playlist(Base):
    __tablename__ = "playlists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str | None]
    picture_url: Mapped[str | None]

    viewers_ids: Mapped[IntArray]
    likers_ids: Mapped[IntArray]

    created_at: Mapped[date]
    updated_at: Mapped[datetime]

    authors: Mapped[list["User"]] = relationship(   # type: ignore[name-defined]  # noqa: F821
        argument="User",
        secondary=author_to_playlists_association,
        back_populates="coauthored_playlists",
        lazy="selectin",
    )
    beats: Mapped[list["Beat"]] = relationship(   # type: ignore[name-defined]  # noqa: F821
        argument="Beat",
        secondary=playlists_to_beat_association,
        lazy="selectin",
    )
    tracks: Mapped[list["Track"]] = relationship(   # type: ignore[name-defined]  # noqa: F821
        argument="Track",
        secondary=playlists_to_track_association,
        lazy="selectin",
    )
    tags: Mapped[list["Tag"]] = relationship(   # type: ignore[name-defined]  # noqa: F821
        argument="Tag",
        secondary=playlists_to_tag_association,
        lazy="selectin",
    )
