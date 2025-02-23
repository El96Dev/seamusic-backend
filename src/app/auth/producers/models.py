from datetime import datetime, date

from sqlalchemy import ForeignKey, Column, Table, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.music.beats.models import producer_to_beat_association
from src.infrastructure.postgres import Base

producers_to_beatpacks_association = Table(
    "producers_to_beatpacks_association",
    Base.metadata,
    Column("producer_profile_id", ForeignKey("producer_profiles.id"), primary_key=True),
    Column("beatpack_id", ForeignKey("beatpacks.id"), primary_key=True),
)

user_to_producer_association = Table(
    "user_to_producer_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("producer_id", Integer, ForeignKey("producer_profiles.id"), primary_key=True),
)

followers_to_producers_association = Table(
    "followers_to_producers_association",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("producer_id", Integer, ForeignKey("producer_profiles.id"), primary_key=True),
)

producers_to_soundkits_association = Table(
    "producers_to_soundkits_association",
    Base.metadata,
    Column("soundkit_id", Integer, ForeignKey("soundkits.id"), primary_key=True),
    Column("producer_id", Integer, ForeignKey("producer_profiles.id"), primary_key=True),
)

producers_to_tags_association = Table(
    "producers_to_tags_association",
    Base.metadata,
    Column("producer_id", ForeignKey("producer_profiles.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

producers_to_squads_association = Table(
    "producers_to_squads_association",
    Base.metadata,
    Column("producer_id", Integer, ForeignKey("producer_profiles.id"), primary_key=True),
    Column("squad_id", Integer, ForeignKey("squads.id"), primary_key=True),
)


class ProducerProfile(Base):
    __tablename__ = "producer_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    description: Mapped[str]
    picture_url: Mapped[str]

    created_at: Mapped[date]
    updated_at: Mapped[datetime]
    is_available: Mapped[bool]

    followers: Mapped[list["User"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="User",
        secondary=followers_to_producers_association,
        back_populates="followed_producers",
        lazy="selectin",
    )
    beats: Mapped[list["Beat"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Beat",
        secondary=producer_to_beat_association,
        back_populates="producers",
        lazy="selectin",
    )
    squads: Mapped[list["Squad"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Squad",
        secondary=producers_to_squads_association,
        back_populates="producers",
        lazy="selectin",
    )
    tags: Mapped[list["Tag"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Tag",
        secondary=producers_to_tags_association,
        lazy="selectin",
    )
    beatpacks: Mapped[list["Beatpack"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Beatpack",
        secondary=producers_to_beatpacks_association,
        back_populates="producers",
        lazy="selectin",
    )
    soundkits: Mapped[list["Soundkit"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Soundkit",
        secondary=producers_to_soundkits_association,
        back_populates="producers",
        lazy="selectin",
    )
