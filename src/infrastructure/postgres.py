from dataclasses import dataclass
from typing import Any, Literal, Annotated

from sqlalchemy import ARRAY, String, Integer
from sqlalchemy import Executable
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.config import settings

engine = create_async_engine(url=settings.db_url, echo=settings.echo)
StringArray = Mapped[Annotated[list[str], mapped_column(ARRAY(String))]]
IntegerArray = Mapped[Annotated[list[int], mapped_column(ARRAY(Integer))]]


class Base(DeclarativeBase):
    __abstract__ = True


@dataclass
class PostgresSessionMixin(AsyncSession):
    table: type[Base]

    async def read(self, obj_id: int) -> Any | None:
        return await self.get(self.table, obj_id)

    async def write(self, obj) -> None:  # type: ignore[no-untyped-def]
        self.add(obj)

    async def update(self, obj: Base) -> None:
        await self.merge(obj)

    async def remove(self, obj_id: int) -> None:
        obj = await self.get(self.table, obj_id)
        await self.delete(obj)

    async def run(self, statement: Executable, action: Literal['scalars', 'scalar', 'execute']):  # type: ignore[no-untyped-def]
        if action == 'scalars':
            return list(await self.scalars(statement))
        elif action == 'scalar':
            return await self.scalar(statement)
        elif action == 'execute':
            await self.execute(statement)
