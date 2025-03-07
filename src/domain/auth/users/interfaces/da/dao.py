from abc import abstractmethod
from datetime import date, datetime
from typing import Self, Literal

from src.domain.auth.users.interfaces.base import BaseInterface
from src.domain.auth.users.interfaces.da.models import BaseUserModel, AccessLevel, PremiumLevel


class DAO(BaseInterface):
    """
    Data Access Object (DAO) is an abstract class created
    to define and describe necessary functions for data acess.

    It's used in services' layer to manipulate storage data.

    As an abstraction, DAO cannot be used directly - that will
    cause `NotImplementedError` and crash the application. So,
    to provide the data access, a DAO implementation is required.

    DAO implementation is a DAO's subclass designed in a unique way
    for an exact type of storage. It can ONLY be used for CRUD
    operations with data in that type of storage. The implementation
    must be provided to the service's layer via factory to avoid using
    globals.
    """

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> BaseUserModel | None:
        """
        Gets user by its identificator

        :param user_id: user's numeric identifecator
        :return BaseUserModel: instance of BaseUserModel subclass
        :raise NotImplementedError: when called directly by abstract class instance
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> BaseUserModel | None:
        """
        Gets user by its identificator

        :param username: custom user's string identifecator
        :return BaseUserModel: instance of BaseUserModel subclass
        :raise NotImplementedError: when called directly by abstract class instance
        """
        raise NotImplementedError

    @abstractmethod
    async def get_users(self) -> list[BaseUserModel]:
        """
        Gets all users

        :return list[BaseUserModel]: list of BaseUserModel subclass' instances
        :raise NotImplementedError: when called directly by abstract class instance
        """
        raise NotImplementedError

    @abstractmethod
    async def count_users(self) -> int:
        """
        Counts users in storage

        :return int: total amount of users in storage
        :raise NotImplementedError: when called directly by abstract class instance
        """
        raise NotImplementedError

    @abstractmethod
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
        followed_tags: list[str],
        telegram_id: int | None = None,
        description: str | None = None,
        picture_url: str | None = None,
    ) -> int:
        """
        Updates an existing user

        :param email: user's email
        :param password: new password
        :param username: custom user's string identificator
        :param description: user profile's bio
        :param created_at: date when account was created
        :param updated_at: date and time when profile was updated for the last time
        :param access_level: level of rights
        :param premium_level: level of premium subscription
        :param is_verified: parameter that is `True` when email is confirmed
        :param telegram_id: numeric primary identificator in telegram
        :param picture_url: URL of a picture in media storage
        :param artist_id: artist's numeric primary identificator
        :param producer_id: producer's numeric primary identificator
        :param licenses_ids: a list of  licenses' numeric primary identificators
        :param followed_squads_ids: a list of followed squads' numeric primary identificators
        :param followed_artists_ids: a list of followed artists' numeric primary identificators
        :param coauthored_playlists_ids: a list of co-authored playlists' numeric primary identificators
        :param saved_playlists_ids: a list of saved playlists' numeric primary identificators
        :param followed_producers_ids: a list of followed producers' numeric primary identificators
        :param saved_albums_ids: a list of saved albums' numeric primary identificators
        :param followed_tags: a list of followed tags
        :return int: user's numeric primary identificator
        :raise NotImplementedError: when called directly by abstract class instance
        """
        raise NotImplementedError

    @abstractmethod
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
        """
        Updates an existing user

        :param user_id: user's numeric primary identificator
        :param username: custom user's string identificator
        :param email: user's email
        :param password: user's password
        :param description: user profile's bio
        :param picture_url: URL of avatar in media storage
        :param created_at: date when account was created
        :param updated_at: date and time when profile was updated for the last time
        :param access_level: level of rights
        :param premium_level: level of premium subscription
        :param artist_id: artist's numeric primary identificator
        :param producer_id: producer's numeric primary identificator
        :param telegram_id: user's telegram identificator
        :param is_verified: parameter that is `True` when email is confirmed
        :param licenses_ids: a list of  licenses' numeric primary identificators
        :param followed_squads_ids: a list of followed squads' numeric primary identificators
        :param followed_artists_ids: a list of followed artists' numeric primary identificators
        :param coauthored_playlists_ids: a list of co-authored playlists' numeric primary identificators
        :param saved_playlists_ids: a list of saved playlists' numeric primary identificators
        :param followed_producers_ids: a list of followed producers' numeric primary identificators
        :param saved_albums_ids: a list of saved albums' numeric primary identificators
        :param followed_tags: a list of followed tags
        :return int: user's numeric primary identificator
        :raise NotImplementedError: when called directly by abstract class instance
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        """
        Deletes an existing user

        :param user_id: user's numeric primary identificator
        :raise NotImplementedError: when called directly by abstract class instance
        """
        raise NotImplementedError

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore[no-untyped-def]
        pass
