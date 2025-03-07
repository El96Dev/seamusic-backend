# from abc import ABC, abstractmethod
# from dataclasses import dataclass
# from datetime import date
# from typing import Callable
#
# from src.domain.auth.users.interfaces.da.dao import DAO
# from src.domain.auth.users.interfaces.ma.mao import MAO
#
#
# @dataclass
# class BaseUsersService(ABC):
#     """
#     BaseUsersService is an abstract class for services' layer of users'
#     management. Its subclasses provide the application's core, its logic.
#     This is the least typical layer in the entire app. Doing it is not
#     a routine(as client-server communication or data access), it's a
#     meaningful process, so keep careful and be sure you checked
#     everything to avoid security issues.
#
#     As an abstraction, `BaseUsersService` cannot be used directly - that will
#     cause `NotImplementedError` and crash the application. So, to provide
#     the application's logic, a service subclass is required.
#
#     :param dao_impl_factory: synchronous function for creating DAO
#       implementations
#     :param mao_impl_factory: synchronous function for creating MAO
#       implementations
#     """
#
#     dao_impl_factory: Callable[[], DAO]
#     mao_impl_factory: Callable[[], MAO]
#
#     @abstractmethod
#     async def get_user_by_id(self, user_id: int) -> BaseUserResponseDTO:
#         """
#         Gets user by its identificator
#
#         :param user_id: user's numeric identificator
#         :return BaseUserResponseDTO: DTO with user's parameters
#         :raise UserNotFoundError: when user doesn't exist in storage
#         :raise NotAuthenticatedError: when current user is not authenticated
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def get_user_by_username(self, username: str) -> BaseUserResponseDTO:
#         """
#         Gets user by its identificator
#
#         :param username: custom user's string identificator
#         :return BaseUserResponseDTO: DTO with user's parameters
#         :raise UserNotFoundError: when user doesn't exist in storage
#         :raise NotAuthenticatedError: when current user is not authenticated
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def get_me(self) -> BaseMeResponse:
#         """
#         Gets currently authorized user
#
#         :return BaseMeResponse: DTO with user's parameters
#         :raise NotAuthenticatedError: when current user is not authenticated
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def get_users(self, start: int, size: int) -> BaseUsersResponseDTO:
#         """
#         Gets and paginates users
#
#         :param start: start point where objects start being taken from storage.
#           Another words, this is just the beginning of the page
#         :param size: object's length
#         :return: DTO with users' sequence
#         :raise NotAuthenticatedError: when current user is not authenticated
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def update_profile_picture(self, data: bytes | None) -> UpdateProfilePictureResponseDTO:
#         """
#         Updates current user's profile picture
#
#         :param data: file data in bytes format
#         :return UpdateProfilePictureResponseDTO: DTO with new user's identificator
#         :raise NotAuthenticatedError: when current user is not authenticated
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def update_user(
#         self,
#         username: str | None = None,
#         description: str | None = None,
#     ) -> UpdateUserResponseDTO:
#         """
#         Updates current user
#
#         :param username: new username
#         :param description: new bio
#         :return UpdateUserResponseDTO: DTO with new user's identificator
#         :raise NotAuthenticatedError: when current user is not authenticated
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
