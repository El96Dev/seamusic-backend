from src.infrastructure.exceptions import Exc


class AlbumNotFoundError(Exc):
    """Album not found"""


class AlbumAlreasyExistsError(Exc):
    """Album already exists"""


class NoArtistProfileError(Exc):
    """You are not an artist"""


class NoRightsError(Exc):
    """Not enough rights for perfoming an operation"""


class AlbumAlreadyLikedError(Exc):
    """Album is already liked"""


class AlbumNotLikedError(Exc):
    """Album is not liked yet"""
