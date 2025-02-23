from datetime import datetime, date

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.app.auth.producers.models import producers_to_beatpacks_association
from src.infrastructure.postgres import Base, IntArray

beatpack_to_beats_association = Table(
    "beatpack_to_beat_association",
    Base.metadata,
    Column("beat_id", ForeignKey("beats.id"), primary_key=True),
    Column("beatpack_id", ForeignKey("beatpacks.id"), primary_key=True),
)

beatpacks_to_tags_association = Table(
    "beatpacks_to_tags_association",
    Base.metadata,
    Column("beatpack_id", ForeignKey("beatpacks.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Beatpack(Base):
    __tablename__ = "beatpacks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str | None]

    viewers_ids: Mapped[IntArray]
    likers_ids: Mapped[IntArray]

    created_at: Mapped[date]
    updated_at: Mapped[datetime]

    producers: Mapped[list["ProducerProfile"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="ProducerProfile",
        secondary=producers_to_beatpacks_association,
        back_populates="beatpacks",
        lazy="selectin",
    )
    beats: Mapped[list["Beat"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Beat",
        secondary=beatpack_to_beats_association,
        lazy="selectin",
    )
    tags: Mapped[list["Tag"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Tag",
        secondary=beatpacks_to_tags_association,
        lazy="selectin",
    )
