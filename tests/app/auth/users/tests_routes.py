from datetime import date, datetime
from tempfile import SpooledTemporaryFile
from typing import Callable, Literal

import pytest
from fastapi import status, UploadFile
from fastapi.testclient import TestClient

from src.app.music.albums.api.routes import Router, get_router
from src.presentation.schemas.music.albums import (
    SCreateAlbumRequest,
    SCreateAlbumResponse,
    SAlbumResponse,
    SUpdateAlbumRequest,
    SUpdateAlbumResponse,
    SPopularAlbumsResponse,
    SUpdateAlbumCoverRequest,
)
from tests.app.music.albums.fixtures import AlbumTestModel, album  # noqa: F401


class TestRouter:
    @pytest.fixture(scope="function")
    def router_factory(self) -> Callable[[], Router]:
        return get_router

    @pytest.fixture(scope="function")
    def album_id(self, album: AlbumTestModel) -> int:
        return album["id"]

    @pytest.fixture(scope="function")
    def album_title(self, album: AlbumTestModel) -> str:
        return album["title"]

    @pytest.fixture(scope="function")
    def album_type(self, album: AlbumTestModel) -> Literal["album", "single"]:
        return album["type"]

    @pytest.fixture(scope="function")
    def album_created_at(self, album: AlbumTestModel) -> date:
        return album["created_at"]

    @pytest.fixture(scope="function")
    def album_updated_at(self, album: AlbumTestModel) -> datetime:
        return album["updated_at"]

    @pytest.fixture(scope="function")
    def album_viewers_ids(self, album: AlbumTestModel) -> list[int]:
        return album["viewers_ids"]

    @pytest.fixture(scope="function")
    def album_likers_ids(self, album: AlbumTestModel) -> list[int]:
        return album["likers_ids"]

    @pytest.fixture(scope="function")
    def album_artists_ids(self, album: AlbumTestModel) -> list[int]:
        return album["artists_ids"]

    @pytest.fixture(scope="function")
    def album_tracks_ids(self, album: AlbumTestModel) -> list[int]:
        return album["tracks_ids"]

    @pytest.fixture(scope="function")
    def album_tags(self, album: AlbumTestModel) -> list[str]:
        return album["tags"]

    @pytest.fixture(scope="function")
    def artist_id(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def album_picture_url(self, album: AlbumTestModel) -> str | None:
        return album["picture_url"]

    @pytest.fixture(scope="function")
    def album_description(self, album: AlbumTestModel) -> str | None:
        return album["description"]

    @pytest.fixture(scope="function")
    def start(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def size(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def user_id(self) -> int:
        return 1

    def test_create_album(  # TODO: add parametrized statuses after auth module is done
        self,
        client: TestClient,
        album: AlbumTestModel,
    ) -> None:
        request_json = SCreateAlbumRequest(
            title=album["title"],
            description=album["description"],
            tags=album["tags"],
        ).__dict__
        response = client.post(url="/albums/", json=request_json)
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_409_CONFLICT,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_401_UNAUTHORIZED,
        ]
        assert isinstance(response.json(), dict)
        if response.status_code == status.HTTP_201_CREATED:
            model = SCreateAlbumResponse(**response.json())
            album["id"] = model.id

    @pytest.mark.parametrize(  # TODO: add other statuses after auth module is done
        'album_id,expected_status',
        [
            (1, status.HTTP_200_OK),
            (100, status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_get_album(
        self,
        client: TestClient,
        album_id: int,
        expected_status: int,
    ) -> None:
        response = client.get(url=f"albums/{album_id}")
        assert response.status_code == expected_status
        assert isinstance(response.json(), dict)
        if expected_status == status.HTTP_200_OK:
            SAlbumResponse(**response.json())

    @pytest.mark.parametrize(  # TODO: add other statuses after auth module is done
        'album_id,expected_status',
        [
            (1, status.HTTP_200_OK),
            (100, status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_update_album(
        self,
        client: TestClient,
        expected_status: int,
        album: AlbumTestModel,
        album_id: int,
        album_title: str,
        album_description: str,
        album_picture_url: str,
        album_artists_ids: list[int],
        album_tracks_ids: list[int],
        album_tags: list[str],
    ) -> None:
        request_json = SUpdateAlbumRequest(
            id=album_id,
            title=album_title,
            description=album_description,
            picture_url=album_picture_url,
            artists_ids=album_artists_ids,
            tracks_ids=album_tracks_ids,
            tags=album_tags,
        ).__dict__
        response = client.put(url=f"/albums/{album_id}", json=request_json)
        assert response.status_code == expected_status
        assert isinstance(response.json(), dict)
        if expected_status == status.HTTP_201_CREATED:
            model = SUpdateAlbumResponse(**response.json())
            album["id"] = model.id

    @pytest.mark.parametrize(  # TODO: add other statuses after auth module is done
        'album_id,expected_status',
        [
            (1, status.HTTP_204_NO_CONTENT),
            (100, status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_like_album(
        self,
        client: TestClient,
        expected_status: int,
        album_id: int,
    ) -> None:
        response = client.patch(f"/albums/{album_id}/like")
        assert response.status_code == expected_status
        assert isinstance(response.json(), dict)

    @pytest.mark.parametrize(  # TODO: add other statuses after auth module is done
        'album_id,expected_status',
        [
            (1, status.HTTP_204_NO_CONTENT),
            (100, status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_unlike_album(
        self,
        client: TestClient,
        expected_status: int,
        album_id: int,
    ) -> None:
        response = client.patch(f"/albums/{album_id}/unlike")
        assert response.status_code == expected_status
        assert isinstance(response.json(), dict)

    def test_get_popular_albums(
        self,
        client: TestClient,
    ) -> None:
        response = client.get("/albums")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), dict)
        SPopularAlbumsResponse(**response.json())

    @pytest.mark.parametrize(  # TODO: add other statuses after auth module is done
        'album_id,expected_status',
        [
            (1, status.HTTP_204_NO_CONTENT),
            (100, status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_update_cover(
        self,
        client: TestClient,
        expected_status: int,
        album_id: int,
    ) -> None:
        request_json = SUpdateAlbumCoverRequest(
            album_id=album_id,
            file=UploadFile(filename='picture.png', file=SpooledTemporaryFile()),  # type: ignore[arg-type]
        ).__dict__
        response = client.post(
            url=f"/albums/{album_id}/cover",
            data=request_json,
        )
        assert response.status_code == expected_status
        assert isinstance(response.json(), dict)

    @pytest.mark.parametrize(  # TODO: add other statuses after auth module is done
        'album_id,expected_status',
        [
            (1, status.HTTP_204_NO_CONTENT),
            (100, status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_delete_album(
        self,
        client: TestClient,
        expected_status: int,
        album_id: int,
    ) -> None:
        response = client.delete(f"/albums/{album_id}")
        assert response.status_code == expected_status
        assert isinstance(response.json(), dict)
