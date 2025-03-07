import pytest

from src.domain.auth.users.interfaces.base import BaseInterface
from src.domain.auth.users.interfaces.da.dao import DAO
from src.domain.auth.users.interfaces.ma.mao import MAO


@pytest.mark.user
@pytest.mark.user_dao
async def test_base_interface_initialization() -> None:
    with pytest.raises(TypeError):
        BaseInterface()


@pytest.mark.user
@pytest.mark.user_dao
async def test_mao_initialization() -> None:
    with pytest.raises(TypeError):
        MAO()  # type: ignore[abstract]


@pytest.mark.user
@pytest.mark.user_dao
async def test_dao_initialization() -> None:
    with pytest.raises(TypeError):
        DAO()  # type: ignore[abstract]
