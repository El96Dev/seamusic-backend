from dataclasses import dataclass
from datetime import date, datetime
from types import TracebackType
from typing import Literal, Self

from sqlalchemy import select, func

from src.app.auth.artists.models import ArtistProfile
from src.app.auth.producers.models import ProducerProfile
from src.app.auth.users.interfaces.da.models import User
from src.app.music.albums.interfaces.da.models import Album
from src.app.music.squads.models import Squad
from src.app.social.licenses.models import License
from src.app.social.playlists.models import Playlist
from src.app.social.tags.models import Tag
from src.domain.auth.users.interfaces.da.dao import DAO
from src.domain.auth.users.interfaces.da.models import AccessLevel, PremiumLevel
from src.infrastructure.loggers import app as logger
from src.infrastructure.postgres import PostgresSessionMixin


@dataclass
class PostgresDAOImplementation(DAO, PostgresSessionMixin):
    def __init__(self) -> None:
        super(PostgresDAOImplementation, self).__init__(table=User)
        self.table = User

    async def get_user_by_id(self, user_id: int) -> User | None:
        logger.info("get_user_by_id DAO request")
        response: User | None = await self.read(obj_id=user_id)
        return response

    async def get_user_by_username(self, username: int) -> User | None:
        logger.info("get_user_by_username DAO request")
        response: User | None = await self.run(
            statement=select(User).group_by(User.id).filter(User.username == username),
            method="scalar",
        )
        return response

    async def get_users(self) -> list[User]:  # type: ignore[override]
        logger.info("get_users DAO request")
        response: list[User] = await self.run(
            statement=select(User).group_by(User.id).order_by(User.updated_at),
            method="scalars",
        )
        return response

    async def count_users(self) -> int:
        logger.info("count_users DAO request")
        response: int = await self.run(
            statement=select(func.count(User.id)),
            method="scalar",
        )
        return response

    async def create_user(
        self,
        email: str,
        password: str,
        username: str,
        created_at: date,
        updated_at: datetime,
        access_level: Literal["user", "admin", "superuser"],
        premium_level: Literal["none", "bot", "full"],
        is_verified: bool,
        artist_id: int,
        producer_id: int,
        licenses_ids: list[int],
        followed_squads_ids: list[int],
        followed_artists_ids: list[int],
        coauthored_playlists_ids: list[int],
        saved_playlists_ids: list[int],
        followed_producers_ids: list[int],
        saved_albums_ids: list[int],
        followed_tags_ids: list[int],
        telegram_id: int | None = None,
        description: str | None = None,
        picture_url: str | None = None,
    ) -> int:
        logger.info("create_user DAO request")
        user = User(
            username=username,
            description=description,
            email=email,
            password=password,
            picture_url=picture_url,
            created_at=created_at,
            updated_at=updated_at,
            access_level=access_level,
            premium_level=premium_level,
            telegram_id=telegram_id,
            is_verified=is_verified,
            artist_id=artist_id,
            producer_id=producer_id,
            artist_profile=await self.run(
                statement=select(ArtistProfile).group_by(ArtistProfile.id).filter(ArtistProfile.id == artist_id),
                method="scalar",
            ),
            producer_profile=await self.run(
                statement=select(ProducerProfile).group_by(ProducerProfile.id).filter(ProducerProfile.id == producer_id),
                method="scalar",
            ),
            licenses=await self.run(
                statement=select(License).group_by(License.id).filter(License.id.in_(licenses_ids)),
                method="scalars",
            ) if licenses_ids else list(),
            followed_squads=await self.run(
                statement=select(Squad).group_by(Squad.id).filter(Squad.id.in_(followed_squads_ids)),
                method="scalars",
            ) if followed_squads_ids else list(),
            followed_artists=await self.run(
                statement=select(ArtistProfile).group_by(ArtistProfile.id).filter(ArtistProfile.id.in_(followed_artists_ids)),
                method="scalars",
            ) if followed_artists_ids else list(),
            coauthored_playlists=await self.run(
                statement=select(Playlist).group_by(Playlist.id).filter(Playlist.id.in_(coauthored_playlists_ids)),
                method="scalars",
            ) if coauthored_playlists_ids else list(),
            saved_playlists=await self.run(
                statement=select(Playlist).group_by(Playlist.id).filter(Playlist.id.in_(saved_playlists_ids)),
                method="scalars",
            ) if saved_playlists_ids else list(),
            followed_producers=await self.run(
                statement=select(ProducerProfile).group_by(ProducerProfile.id).filter(ProducerProfile.id.in_(followed_producers_ids)),
                method="scalars",
            ) if followed_producers_ids else list(),
            saved_albums=await self.run(
                statement=select(Album).group_by(Album.id).filter(Album.id.in_(saved_albums_ids)),
                method="scalars",
            ) if saved_albums_ids else list(),
            followed_tags=await self.run(
                statement=select(Tag).group_by(Tag.id).filter(Tag.id.in_(followed_tags_ids)),
                method="scalars",
            ) if followed_tags_ids else list(),
        )
        await self.create(user)
        return user.id

    async def update_user(
        self,
        user_id: int,
        username: str | None = None,
        description: str | None = None,
        email: str | None = None,
        password: str | None = None,
        picture_url: str | None = None,
        created_at: date | None = None,
        updated_at: datetime | None = None,
        access_level: AccessLevel | None = None,
        premium_level: PremiumLevel | None = None,
        artist_id: int | None = None,
        producer_id: int | None = None,
        telegram_id: int | None = None,
        is_verified: bool | None = None,
        licenses_ids: list[int] | None = None,
        followed_squads_ids: list[int] | None = None,
        followed_artists_ids: list[int] | None = None,
        coauthored_playlists_ids: list[int] | None = None,
        saved_playlists_ids: list[int] | None = None,
        followed_producers_ids: list[int] | None = None,
        saved_albums_ids: list[int] | None = None,
        followed_tags: list[str] | None = None,
    ) -> int:
        logger.info("update_user DAO request")
        user = User(**dict(filter(
            lambda item: bool(item[1]),
            {
                "id": user_id,
                "username": username if username else None,
                "description": description if description else None,
                "email": email if email else None,
                "password": password if password else None,
                "picture_url": picture_url if picture_url else None,
                "created_at": created_at if created_at else None,
                "updated_at": updated_at if updated_at else None,
                "access_level": str(access_level) if access_level else None,
                "premium_level": str(premium_level) if premium_level else None,
                "artist_id": artist_id if artist_id else None,
                "producer_id": producer_id if producer_id else None,
                "telegram_id": telegram_id if telegram_id else None,
                "is_verified": is_verified if is_verified else None,
                "artist_profile": await self.run(
                    statement=select(ArtistProfile).group_by(ArtistProfile.id).filter(ArtistProfile.id == artist_id),
                    method="scalar",
                ) if artist_id else None,
                "profile_profile": await self.run(
                    statement=select(ProducerProfile).group_by(ProducerProfile.id).filter(ProducerProfile.id == producer_id),
                    method="scalar",
                ),
                "licenses": await self.run(
                    statement=select(License).group_by(License.id).filter(License.id.in_(licenses_ids)),
                    method="scalars",
                ) if licenses_ids else list(),
                "followed_squads": await self.run(
                    statement=select(Squad).group_by(Squad.id).filter(Squad.id.in_(followed_squads_ids)),
                    method="scalars",
                ) if followed_squads_ids else list(),
                "followed_artists": await self.run(
                    statement=select(ArtistProfile).group_by(ArtistProfile.id).filter(ArtistProfile.id.in_(followed_artists_ids)),
                    method="scalars",
                ) if followed_artists_ids else list(),
                "coauthored_playlists": await self.run(
                    statement=select(Playlist).group_by(Playlist.id).filter(Playlist.id.in_(coauthored_playlists_ids)),
                    method="scalars",
                ) if coauthored_playlists_ids else list(),
                "saved_playlists": await self.run(
                    statement=select(Playlist).group_by(Playlist.id).filter(Playlist.id.in_(saved_playlists_ids)),
                    method="scalars",
                ) if saved_playlists_ids else list(),
                "followed_producers": await self.run(
                    statement=select(ProducerProfile).group_by(ProducerProfile.id).filter(ProducerProfile.id.in_(followed_producers_ids)),
                    method="scalars",
                ) if followed_producers_ids else list(),
                "saved_albums": await self.run(
                    statement=select(Album).group_by(Album.id).filter(Album.id.in_(saved_albums_ids)),
                    method="scalars",
                ) if saved_albums_ids else list(),
                "followed_tags": await self.run(
                    statement=select(Tag).group_by(Tag.id).filter(Tag.name.in_(followed_tags)),
                    method="scalars",
                ) if followed_tags else list(),
            }.items()
        )))
        await self.create(user)
        return user.id

    async def delete_user(self, user_id: int) -> None:
        logger.info("delete_user DAO request")
        await self.delete_(obj_id=user_id)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[Exception],
        exc_val: Exception,
        exc_tb: TracebackType,
    ) -> None:
        await self.commit()
        await self.close()


def get_postgres_dao_implementation() -> PostgresDAOImplementation:
    """
    :return: instance of PostgresDAOImplementation
    """
    return PostgresDAOImplementation()
