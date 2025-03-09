from dataclasses import dataclass
from typing import Any, Literal, Annotated

from sqlalchemy import ARRAY, String, Integer, Executable
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, mapped_column

from src.infrastructure.config import settings

engine = create_async_engine(url=settings.db_url, echo=settings.echo)
StrArray = Annotated[list[str], mapped_column(ARRAY(String))]
IntArray = Annotated[list[int], mapped_column(ARRAY(Integer))]
Base = declarative_base()


@dataclass
class PostgresSessionMixin(AsyncSession):
    """
    PostgresSessionMixin is a mixin class for database interface
    implementation that is designed to use postgres there and
    should only be used via its subclass' asynchronous context
    manager
    """

    def __init__(self, table: type[Base]) -> None:  # type: ignore[valid-type]
        super(PostgresSessionMixin, self).__init__(bind=engine)
        self.table = table

    async def read(self, obj_id: int) -> Any | None:
        return await self.get(self.table, obj_id)

    async def create(self, obj) -> None:  # type: ignore[no-untyped-def]
        self.add(obj)

    async def update(self, obj: Base) -> None:  # type: ignore[valid-type]
        await self.merge(obj)

    async def delete_(self, obj_id: int) -> None:
        obj = await self.get(self.table, obj_id)
        await self.delete(obj)

    async def run(self, statement: Executable, method: Literal['scalars', 'scalar', 'execute']):  # type: ignore[no-untyped-def]
        if method == 'scalars':
            return list(await self.scalars(statement))
        elif method == 'scalar':
            return await self.scalar(statement)
        elif method == 'execute':
            await self.execute(statement)
