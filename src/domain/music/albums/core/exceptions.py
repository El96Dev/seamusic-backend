from src.infrastructure.exceptions import Exc


class AlbumNotFoundError(Exc):
    """Album not found"""


class AlbumAlreasyExistsError(Exc):
    """Album already exists"""


class NoArtistRightsError(Exc):
    """You are not an artist"""
