from datetime import datetime

from sqlalchemy import Column, Integer, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.social.chats.models import message_to_chat_association
from src.infrastructure.postgres import Base

author_to_messages_association = Table(
    "author_to_messages_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("message_id", Integer, ForeignKey("messages.id"), primary_key=True),
)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    chat: Mapped["Chat"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        argument="Chat",
        secondary=message_to_chat_association,
        back_populates="messages",
        lazy="selectin",
    )
    author: Mapped["User"] = relationship(   # type: ignore[name-defined]  # noqa: F821
        argument="User",
        secondary=author_to_messages_association,
        back_populates="messages",
        lazy="selectin",
    )
