from datetime import datetime, date

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.app.music.beatpacks.models import beatpack_to_beats_association, Beatpack
from src.app.social.tags.models import Tag
from src.infrastructure.postgres import Base, IntArray

tag_to_beat_association = Table(
    "tag_to_beat_association",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    Column("beat_id", ForeignKey("beats.id"), primary_key=True),
)

producer_to_beat_association = Table(
    "producer_to_beat_association",
    Base.metadata,
    Column("producer_id", ForeignKey("producer_profiles.id"), primary_key=True),
    Column("beat_id", ForeignKey("beats.id"), primary_key=True),
)


class Beat(Base):
    __tablename__ = "beats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str | None]
    picture_url: Mapped[str | None]
    file_url: Mapped[str]

    viewers_ids: Mapped[IntArray]
    likers_ids: Mapped[IntArray]

    created_at: Mapped[date]
    updated_at: Mapped[datetime]

    producers: Mapped[list["ProducerProfile"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="ProducerProfile",
        secondary=producer_to_beat_association,
        back_populates="beats",
        lazy="selectin",
    )
    beatpacks: Mapped[list[Beatpack]] = relationship(
        argument="Beatpack",
        secondary=beatpack_to_beats_association,
        back_populates="beats",
        lazy="selectin",
    )
    tags: Mapped[list["Tag"]] = relationship(
        argument="Tag",
        secondary=tag_to_beat_association,
        lazy="selectin",
    )
