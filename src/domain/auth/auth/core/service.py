# from abc import ABC, abstractmethod
# from dataclasses import dataclass
# from datetime import date
# from typing import Callable
#
# from src.domain.auth.auth.interfaces.da.dao import DAO
# from src.domain.auth.auth.interfaces.email.client import BaseEmailClient
#
#
# @dataclass
# class BaseAuthService(ABC):
#     """
#     BaseAuthService is an abstract class for services' layer of
#     authentication. Its subclasses provide the application's core, its
#     logic. This is the least typical layer in the entire app. Doing it
#     is not a routine(as client-server communication or data access),
#     it's a meaningful process, so keep careful and be sure you checked
#     everything to avoid security issues.
#
#     As an abstraction, `BaseAuthService` cannot be used directly - that will
#     cause `NotImplementedError` and crash the application. So, to provide
#     the application's logic, a service subclass is required.
#
#     :param dao_impl_factory: synchronous function for creating DAO
#       implementations
#     :param email_client_factory: synchronous function for creating email
#       client
#     """
#
#     dao_impl_factory: Callable[[], DAO]
#     email_client_factory: Callable[[], BaseEmailClient]
#
#     @abstractmethod
#     async def sign_up(
#         self,
#         email: str,
#         password: str,
#         username: str,
#         description: str | None,
#         birthday: date,
#     ) -> SignUpResponseDTO:
#         """
#         Creates an account
#
#         :param email: user's email adress
#         :param password: new password
#         :param username: new unique custom username
#         :param description: optional profile bio
#         :param birthday: date of birth
#         :return SignUpResponseDTO: DTO with new user's identificator
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def confirm_sign_up(self, token: str) -> ConfirmSignUpResponseDTO:
#         """
#         Confirms signing up and performs an operation
#
#         :param token: token for confirmation
#         :return ConfirmSignUpResponseDTO: DTO with tokens
#         :raise IncorrectCredentialsError: when token does not exist
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def sign_in(self, email: str, password: str) -> None:
#         """
#         Signs in account
#
#         :param email: user's email
#         :param password: user's password
#         :raise IncorrectCredentialsError: when the email does not match the password
#         :raise UserNotFoundError: when user with this email does not exist
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def confirm_sign_in(self, token: str) -> ConfirmSignInResponseDTO:
#         """
#         Confirms signing in and performs an operation
#
#         :param token: token for confirmation
#         :return ConfirmSignInResponseDTO: DTO with tokens
#         :raise IncorrectCredentialsError: when token does not exist
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def update_credentials(
#         self,
#         email: str | None = None,
#         password: str | None = None,
#         telegram_username: str | None = None,
#     ) -> None:
#         """
#         Updates email and password
#
#         :param email: user's new email
#         :param password: user's new password
#         :param telegram_username: telegram's username
#         :raise NotAuthenticatedError: when current user is not authenticated
#         :raise IncorrectCredentialsError: when the email does not match the password
#         :raise UserNotFoundError: when user with this email does not exist
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def confirm_update_credentoals(self, token: str) -> ConfirmUpdateCredentialsResponseDTO:
#         """
#         Confirms signing in and performs an operation
#
#         :param token: token for confirmation
#         :return ConfirmUpdateCredentialsResponseDTO: DTO with new user's identificator
#         :raise IncorrectCredentialsError: when token does not exist
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def delete_account(self) -> None:
#         """
#         Deletes an account
#
#         :raise NotAuthenticatedError: when current user is not authenticated
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
#
#     @abstractmethod
#     async def confirm_deletion(self, token: str) -> ConfirmDeletionResponseDTO:
#         """
#         Confirms deleting an account and performs an operation
#
#         :param token: token for confirmation
#         :return ConfirmDeletionResponseDTO: DTO with tokens
#         :raise IncorrectCredentialsError: when token does not exist
#         :raise NotImplementedError: when called directly by abstract class instance
#         """
#         raise NotImplementedError
