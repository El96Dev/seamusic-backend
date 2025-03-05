from datetime import date, datetime

from sqlalchemy import Table, ForeignKey, Integer, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.app.auth.producers.models import producers_to_squads_association
from src.infrastructure.postgres import Base

follower_to_squads_association = Table(
    "follower_to_squads_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("squad_id", Integer, ForeignKey("squads.id"), primary_key=True)
)

artist_to_squad_association = Table(
    "artist_to_squad_association",
    Base.metadata,
    Column("artist_id", Integer, ForeignKey("artist_profiles.id"), primary_key=True),
    Column("squad_id", Integer, ForeignKey("squads.id"), primary_key=True)
)


class Squad(Base):
    __tablename__ = "squads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str | None]
    picture_url: Mapped[str | None]

    created_at: Mapped[date]
    updated_at: Mapped[datetime]

    followers: Mapped[list["User"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="User",
        secondary=follower_to_squads_association,
        lazy="selectin",
    )
    artists: Mapped[list["ArtistProfile"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="ArtistProfile",
        secondary=artist_to_squad_association,
        back_populates="squads",
        lazy="selectin",
    )
    producers: Mapped[list["ProducerProfile"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="ProducerProfile",
        secondary=producers_to_squads_association,
        back_populates="squads",
        lazy="selectin",
    )
