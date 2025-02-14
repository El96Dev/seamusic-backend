import pytest
from fastapi.testclient import TestClient

from src.app.main import app


@pytest.fixture(scope="function")
def client() -> TestClient:
    return TestClient(app=app)


@pytest.fixture(scope='session')
async def user_id() -> int:
    pytest.skip('skip, user not created')


@pytest.fixture(scope='session')
async def artists_id() -> int:
    pytest.skip('skip, artist not created')
