from dataclasses import dataclass
from datetime import date, datetime
from typing import Self, Literal

from sqlalchemy import select, func

from src.app.auth.artists.models import ArtistProfile
from src.app.auth.users.models import User
from src.app.music.albums.interfaces.da.models import Album
from src.app.music.tracks.models import Track
from src.app.social.tags.models import Tag
from src.domain.music.albums.interfaces.da.dao import DAO
from src.infrastructure.loggers import app as logger
from src.infrastructure.postgres import PostgresSessionMixin


@dataclass
class PostgresDAOImplementation(PostgresSessionMixin, DAO):
    def __init__(self) -> None:
        super(PostgresDAOImplementation, self).__init__(table=Album)
        self.table = Album

    async def get_album_by_id(self, album_id: int) -> Album | None:
        logger.info("get_album_by_id DAO request")
        response: Album | None = await self.read(obj_id=album_id)
        return response

    async def get_album_existance_by_title(self, artist_id: int, title: str) -> bool:
        logger.info("get_album_existance_by_title DAO request")
        return bool(await self.run(select(Album).group_by(Album.id).filter(Album.title == title, Album.artists.any() == artist_id), "scalar"))

    async def get_album_existance_by_id(self, album_id: int) -> bool:
        logger.info("get_album_existance_by_id DAO request")
        return bool(await self.run(select(Album).group_by(Album.id).filter(Album.id == album_id), "scalar"))

    async def get_popular_albums(self, start: int, size: int) -> list[Album]:  # type: ignore[override]
        logger.info("get_popular_albums DAO request")
        return await self.run(select(Album).group_by(Album.id).order_by(func.count(Album.viewers_ids)).offset(start - 1).limit(size), "scalars")

    async def count_albums(self) -> int:
        logger.info("count_albums DAO request")
        return await self.run(select(func.count(Album.id).group_by(Album.id)), "scalar")

    async def get_artist_id_by_user_id(self, user_id: int) -> int | None:
        logger.info("get_artist_id_by_user_id DAO request")
        return await self.run(select(User.artist_id).group_by(User.id).filter(User.id == user_id), "scalar")

    async def create_album(
        self,
        title: str,
        album_type: Literal['album', 'single'],
        created_at: date,
        updated_at: datetime,
        viewers_ids: list[int],
        likers_ids: list[int],
        artists_ids: list[int],
        tracks_ids: list[int],
        tags: list[str],
        picture_url: str | None = None,
        description: str | None = None,
    ) -> int:
        logger.info("create_album DAO request")
        album = Album(
            title=title,
            type=album_type,
            created_at=created_at,
            updated_at=updated_at,
            viewers_ids=viewers_ids,
            likers_ids=likers_ids,
            artists=await self.run(select(ArtistProfile).filter(ArtistProfile.id.in_(artists_ids)), "scalars"),
            tracks=await self.run(select(Track).filter(Track.id.in_(tracks_ids)), "scalars"),
            tags=await self.run(select(Tag).filter(Tag.name.in_(tags)), "scalars"),
            picture_url=picture_url,
            description=description,
        )
        await self.create(album)
        return album.id

    async def update_album(
        self,
        album_id: int,
        title: str | None = None,
        picture_url: str | None = None,
        description: str | None = None,
        album_type: Literal['album', 'single'] | None = None,
        created_at: date | None = None,
        updated_at: datetime | None = None,
        viewers_ids: list[int] | None = None,
        likers_ids: list[int] | None = None,
        artists_ids: list[int] | None = None,
        tracks_ids: list[int] | None = None,
        tags: list[str] | None = None,
    ) -> int:
        logger.info("update_album DAO request")
        album = Album(**dict(filter(
            lambda item: bool(item[1]),
            {
                "id": album_id,
                "title": title,
                "type": album_type,
                "created_at": created_at,
                "updated_at": updated_at,
                "viewers_ids": viewers_ids,
                "likers_ids": likers_ids,
                "artists": await self.run(select(ArtistProfile).filter(ArtistProfile.id.in_(artists_ids)), "scalars") if artists_ids else None,
                "tracks": await self.run(select(Track).filter(Track.id.in_(tracks_ids)), "scalars") if tracks_ids else None,
                "tags": await self.run(select(Tag).filter(Tag.name.in_(tags)), "scalars") if tags else None,
                "picture_url": picture_url,
                "description": description,
            }.items(),
        )))
        await self.update(album)
        return album.id

    async def delete_album(self, album_id: int) -> None:
        logger.info("delete_album DAO request")
        await self.delete_(obj_id=album_id)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore[no-untyped-def]
        await self.commit()
        await self.close()


def get_postgres_dao_implementation() -> PostgresDAOImplementation:
    """
    :return: instance of PostgresDAOImplementation
    """
    return PostgresDAOImplementation()
