from datetime import datetime, date

from sqlalchemy import Table, ForeignKey, Integer, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.infrastructure.postgres import Base

author_to_licenses_association = Table(
    "author_to_licenses_association",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("license_id", Integer, ForeignKey("licenses.id"), primary_key=True),
)

class License(Base):
    __tablename__ = "licenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    text: Mapped[str]
    description: Mapped[str]

    created_at: Mapped[date]
    updated_at: Mapped[datetime]

    author: Mapped["User"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="User",
        secondary=author_to_licenses_association,
        back_populates="licenses",
        lazy="selectin",
    )
