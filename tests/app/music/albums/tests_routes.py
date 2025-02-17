from typing import TypedDict

from fastapi.testclient import TestClient
from fastapi import status
import pytest

from src.domain.music.albums.core.exceptions import AlbumNotFoundError


class AlbumTestModel(TypedDict):
    """
        TypedDict class for check types
    """
    album_id: int | None
    album_title: str
    album_description: str
    album_tags: list[str]
    artists_ids: list[int]
    tracks_ids: list[int]


class TestAlbumRoutes:
    """
        Fixtures
    """

    @pytest.fixture(scope='session')
    async def fixture_user_id(self) -> int:
        return 1

    @pytest.fixture(scope='session')
    async def fixture_artists_id(self) -> int:
        return 1

    @pytest.fixture(scope='session')
    def fixture_album_title(self) -> str:
        return 'title'

    @pytest.fixture(scope='session')
    def fixture_album_description(self) -> str:
        return 'description'

    @pytest.fixture(scope='session')
    def fixture_album_tags(self) -> list[str]:
        return ['one tag', 'two tag']

    @pytest.fixture(scope='session')
    def fixture_artists_ids(self) -> list[int]:
        return []

    @pytest.fixture(scope='session')
    def fixture_tracks_ids(self) -> list[int]:
        return []

    @pytest.fixture(scope='session')
    def fixture_artist_id(self) -> int:
        return 1

    @pytest.fixture(scope='session')
    def fixture_image_bytes(self) -> bytes:
        f = open('album_photo.jpg', 'rb')
        return f.read()

    @pytest.fixture(scope='session')
    def fixture_picture_url(self) -> str:
        return 'https://vk.com/image.png'

    @pytest.fixture(scope='session')
    def fixture_album_dict(
            self,
            fixture_album_title: str,
            fixture_album_description: str,
            fixture_album_tags,
            fixture_artists_ids,
            fixture_tracks_ids
    ) -> dict:
        return {
            'album_id': None,
            'title': fixture_album_title,
            'description': fixture_album_description,
            'tags': fixture_album_tags,
            'artists_ids': fixture_artists_ids,
            'tracks_ids': fixture_tracks_ids
        }

    """
        Testing functions
    """

    def test_create_album(
            self,
            client: TestClient,
            fixture_album_dict: AlbumTestModel
    ):
        response = client.post('/albums/new', json=fixture_album_dict.__dict__)
        response_json = response.json()
        response_status = response.status_code
        assert response_status == status.HTTP_201_CREATED and isinstance(response_json, dict)
        fixture_album_dict['album_id'] = response_json['id']

    def test_get_album(
            self,
            client: TestClient,
            fixture_album_dict: AlbumTestModel
    ):
        response = client.get(f"albums/{fixture_album_dict['album_id']}")
        response_json = response.json()
        response_status = response.status_code
        assert response_status == status.HTTP_200_OK and isinstance(response_json, dict)

    def test_view_for_album(
            self,
            client: TestClient,
            fixture_album_dict: AlbumTestModel
    ):
        response = client.get(f"albums/{fixture_album_dict['album_id']}")
        response_json = response.json()
        assert response_json['views'] >= 1

    def test_update_album(
            self,
            client: TestClient,
            fixture_album_dict: AlbumTestModel,
            fixture_album_title: str,
            fixture_album_description: str,
            fixture_picture_url: str,
            fixture_artists_ids: list[int],
            fixture_tracks_ids: list[int],
            fixture_album_tags: list[str]
    ):
        send_body = {
            'id': fixture_album_dict['album_id'],
            'title': fixture_album_title,
            'description': fixture_album_description,
            'picture_url': fixture_picture_url,
            'artists_ids': fixture_artists_ids,
            'track_ids': fixture_tracks_ids,
            'tags': fixture_album_tags
        }
        response = client.put(f"/albums/{fixture_album_dict['album_id']}", json=send_body)
        response_json = response.json()
        response_code = response.status_code
        assert response_code == status.HTTP_201_CREATED and isinstance(response_json, dict)

    def test_get_artist_albums(
            self,
            client: TestClient,
            fixture_artist_id: int
    ):
        response = client.get(f"/albums/artist/{fixture_artist_id}")
        response_json = response.json()
        response_code = response.status_code
        assert response_code == status.HTTP_200_OK and response_json['total'] >= 1

    def test_like_album(
            self,
            client: TestClient,
            fixture_album_dict: AlbumTestModel
    ):
        response_like = client.patch(f"/albums/{fixture_album_dict['album_id']}/like")
        if response_like.status_code != status.HTTP_202_ACCEPTED:
            raise False
        response_get_by_id = client.get(f"/albums/{fixture_album_dict['album_id']}")
        response_get_by_id_json = response_get_by_id.json()
        assert response_get_by_id_json['likes'] >= 1

    def test_unlike_album(
            self,
            client: TestClient,
            fixture_album_dict: AlbumTestModel
    ):
        response_get_by_id = client.get(f"/albums/{fixture_album_dict['album_id']}")
        likes = response_get_by_id.json()['likes']
        if likes == 0:
            raise Exception("like equals zero")
        response = client.patch(f"/albums/{fixture_album_dict['album_id']}/unlike")
        if response.status_code == status.HTTP_202_ACCEPTED:
            assert False
        new_likes = client.get(f"/albums/{fixture_album_dict['album_id']}").json()['likes']
        assert likes - 1 == new_likes

    def test_get_popular_albums(
            self,
            client: TestClient
    ):
        response = client.get('/albums')
        response_json = response.json()
        response_code = response.status_code
        assert response_code == status.HTTP_200_OK and response_json['total'] >= 1

    def test_update_cover(
            self,
            client: TestClient,
            fixture_album_dict: AlbumTestModel
    ):
        with open('files/avatar.jpg', 'rb') as file:
            response = client.post(
                f"/albums/{fixture_album_dict['album_id']}/cover",
                files={'file': file}
            )
            assert response.status_code == status.HTTP_202_ACCEPTED

    def test_delete_album(
            self,
            client: TestClient,
            fixture_album_dict: AlbumTestModel
    ):
        client.delete(f"/albums/{fixture_album_dict['album_id']}")
        try:
            client.get(f"/albums/{fixture_album_dict['album_id']}")
        except AlbumNotFoundError:
            assert True
        assert False
