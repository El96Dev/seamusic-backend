from types import NoneType
from typing import Literal

import pytest
from sqlalchemy import Executable, select

from src.app.social.tags.models import Tag
from src.infrastructure.postgres import PostgresSessionMixin


@pytest.mark.infrastructure
@pytest.mark.postgres
class TestPostgresSessionMixin:
    @pytest.fixture(scope="function")
    def mixin(self) -> PostgresSessionMixin:
        return PostgresSessionMixin(table=Tag)

    @pytest.fixture(scope="function")
    def obj_id(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def statement(self, obj_id: int) -> Executable:
        return select(Tag).filter(Tag.id == obj_id)

    async def test_create(self, obj: Tag, mixin: PostgresSessionMixin) -> None:
        async with mixin as session:
            await session.create(obj)

    @pytest.mark.parametrize(
        "obj_id,expected_type",
        [(1, Tag), (100, NoneType)]
    )
    async def test_read(
        self,
        obj_id: int,
        mixin: PostgresSessionMixin,
        expected_type: type,
    ) -> None:
        async with mixin as session:
            response = await session.read(obj_id=obj_id)
        assert isinstance(response, expected_type)

    async def test_update(self, obj: Tag, mixin: PostgresSessionMixin) -> None:
        async with mixin as session:
            await session.update(obj)

    async def test_delete(self, obj_id: int, mixin: PostgresSessionMixin) -> None:
        async with mixin as session:
            await session.delete_(obj_id=obj_id)

    @pytest.mark.parametrize(
        "method,expected_type",
        [
            ("scalar", Tag),
            ("scalars", list[Tag])
        ]
    )
    async def test_run(
        self,
        statement: Executable,
        method: Literal['scalars', 'scalar', 'execute'],
        mixin: PostgresSessionMixin,
        expected_type: type,
    ) -> None:
        async with mixin as session:
            response = await session.run(statement, method)
        assert isinstance(response, expected_type)
