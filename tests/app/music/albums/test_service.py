import pytest
from src.app.music.albums.core.service import get_service
from src.domain.music.albums.core.service import BaseService


class TestAlbumService:
    @pytest.fixture(scope='session')
    def album_service_factory(self) -> BaseService:
        return get_service()
