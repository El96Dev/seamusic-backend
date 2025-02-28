from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from src.app.music.albums.api.utils import CurrentUser, get_current_user
from src.app.music.albums.core.service import get_service
from src.domain.music.albums.api.routes import BaseRouter
from src.domain.music.albums.core.exceptions import (
    AlbumNotFoundError,
    AlbumAlreasyExistsError,
    NoArtistRightsError,
)
from src.domain.music.albums.core.service import BaseService
from src.infrastructure.api import ExceptionHandler
from src.infrastructure.exceptions import Exc
from src.infrastructure.loggers import app as logger
from src.presentation.music.albums.schemas import (
    SAlbumRequest,
    SAlbumResponse,
    SArtist,
    STrack,
    SAlbumItemResponse,
    SPopularAlbumsResponse,
    SItemsRequest,
    SUpdateAlbumCoverRequest,
    SLikeAlbumRequest,
    SCreateAlbumRequest,
    SCreateAlbumResponse,
    SUpdateAlbumRequest,
    SUpdateAlbumResponse,
    SDeleteAlbumRequest,
    SUnlikeAlbumRequest,
)

router_v1 = APIRouter(prefix="/albums", tags=["tags"])


def exceptions() -> dict[type[Exc], HTTPException]:
    return {
        AlbumNotFoundError: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{
            "loc": ["string", 0],
            "msg": "Album not found",
            "type": "string",
        }]),
        AlbumAlreasyExistsError: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[{
            "loc": ["string", 0],
            "msg": "Album alreasy exists",
            "type": "string",
        }]),
        NoArtistRightsError: HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=[{
            "loc": ["string", 0],
            "msg": "You don't have an artist profile",
            "type": "string",
        }]),
    }


def examples() -> dict:
    return {
        status.HTTP_404_NOT_FOUND: {"example": {
            "detail": [{
                "loc": ["string", 0],
                "msg": "Album not found",
                "type": "string",
            }]
        }},
        status.HTTP_409_CONFLICT: {"example": {
            "detail": [{
                "loc": ["string", 0],
                "msg": "Album alreasy exists",
                "type": "string",
            }]
        }},
        status.HTTP_403_FORBIDDEN: {"example": {
            "detail": [{
                "loc": ["string", 0],
                "msg": "You don't have an artist profile",
                "type": "string",
            }]
        }},
    }


@asynccontextmanager
async def exception_handler() -> AsyncGenerator[ExceptionHandler, None]:
    async with ExceptionHandler(exceptions=exceptions()) as handler:
        yield handler


@dataclass
class Router(BaseRouter):
    @staticmethod
    @router_v1.get(
        path="/{album_id}",
        summary="Get an album by it's id",
        responses={
            status.HTTP_200_OK: {"model": SAlbumResponse},
            status.HTTP_404_NOT_FOUND: {"content": {"application/json": examples()[status.HTTP_404_NOT_FOUND]}},
        },
    )
    async def get_album(  # type: ignore[override]
        request: SAlbumRequest = Depends(SAlbumRequest),
        service: BaseService = Depends(get_service),
        current_user: CurrentUser = Depends(get_current_user),
    ) -> SAlbumResponse:
        logger.info("get_album API request")
        async with exception_handler():
            album = await service.get_album(album_id=request.album_id, user_id=current_user.id)
        return SAlbumResponse(
            id=album.id,
            title=album.title,
            picture_url=album.picture_url,
            description=album.description,
            type=album.type,
            views=album.views,
            likes=album.likes,
            created_at=album.created_at,
            updated_at=album.updated_at,
            artists=list(map(
                lambda artist: SArtist(
                    id=artist.id,
                    username=artist.username,
                    description=artist.description,
                    picture_url=artist.picture_url,
                    user_id=artist.user_id,
                ),
                list(album.artists),
            )),
            tracks=list(map(
                lambda track: STrack(
                    id=track.id,
                    title=track.title,
                    description=track.description,
                    picture_url=track.picture_url,
                    file_url=track.file_url,
                    views=track.views,
                    likes=track.likes,
                    created_at=track.created_at,
                    updated_at=track.updated_at,
                ),
                list(album.tracks),
            )),
            tags=list(album.tags),
        )

    @staticmethod
    @router_v1.get(
        path="/",
        summary="Get popular albums",
        responses={
            status.HTTP_200_OK: {"model": SPopularAlbumsResponse},
        },
    )
    async def get_popular_albums(  # type: ignore[override]
        page: SItemsRequest = Depends(SItemsRequest),
        service: BaseService = Depends(get_service),
        current_user: CurrentUser = Depends(get_current_user),
    ) -> SPopularAlbumsResponse:
        logger.info("get_popular_albums API request")
        async with exception_handler():
            albums = await service.get_popular_albums(user_id=current_user.id, start=page.start, size=page.size)
        return SPopularAlbumsResponse(
            has_next=albums.has_next,
            has_previous=albums.has_previous,
            total=albums.total,
            page=albums.page,
            size=albums.size,
            items=list(map(
                lambda album: SAlbumItemResponse(
                    id=album.id,
                    title=album.title,
                    picture_url=album.picture_url,
                    description=album.description,
                    views=album.views,
                    likes=album.likes,
                    type=album.type,
                    created_at=album.created_at,
                    updated_at=album.updated_at,
                ),
                albums.items,
            ))
        )

    @staticmethod
    @router_v1.put(
        path="/{album_id}/cover",
        summary="Update an album cover",
        responses={
            status.HTTP_204_NO_CONTENT: {"model": None},
            status.HTTP_404_NOT_FOUND: {"content": {"application/json": examples()[status.HTTP_404_NOT_FOUND]}},
        },
    )
    async def update_cover(  # type: ignore[override]
        request: SUpdateAlbumCoverRequest = Depends(SUpdateAlbumCoverRequest),
        service: BaseService = Depends(get_service),
        current_user: CurrentUser = Depends(get_current_user),
    ) -> None:
        logger.info("update_cover API request")
        async with exception_handler():
            await service.update_cover(
                album_id=request.album_id,
                user_id=current_user.id,
                data=await request.file.read()
            )

    @staticmethod
    @router_v1.patch(
        path="/{album_id}/like",
        summary="Like an album",
        responses={
            status.HTTP_204_NO_CONTENT: {"model": None},
            status.HTTP_404_NOT_FOUND: {"content": {"application/json": examples()[status.HTTP_404_NOT_FOUND]}},
        },
    )
    async def like_album(  # type: ignore[override]
        request: SLikeAlbumRequest = Depends(SLikeAlbumRequest),
        service: BaseService = Depends(get_service),
        current_user: CurrentUser = Depends(get_current_user),
    ) -> None:
        logger.info("like_album API request")
        async with exception_handler():
            await service.like_album(
                user_id=current_user.id,
                album_id=request.album_id,
            )

    @staticmethod
    @router_v1.patch(
        path="/{album_id}/unlike",
        summary="Unlike an album",
        responses={
            status.HTTP_204_NO_CONTENT: {"model": None},
            status.HTTP_404_NOT_FOUND: {"content": {"application/json": examples()[status.HTTP_404_NOT_FOUND]}},
        },
    )
    async def unlike_album(  # type: ignore[override]
        request: SUnlikeAlbumRequest = Depends(SLikeAlbumRequest),
        service: BaseService = Depends(get_service),
        current_user: CurrentUser = Depends(get_current_user),
    ) -> None:
        logger.info("unlike_album API request")
        async with exception_handler():
            await service.unlike_album(
                user_id=current_user.id,
                album_id=request.album_id,
            )

    @staticmethod
    @router_v1.post(
        path="/",
        summary="Create a new album",
        responses={
            status.HTTP_201_CREATED: {"model": SCreateAlbumResponse},
            status.HTTP_403_FORBIDDEN: {"content": {"application/json": examples()[status.HTTP_403_FORBIDDEN]}},
            status.HTTP_409_CONFLICT: {"content": {"application/json": examples()[status.HTTP_409_CONFLICT]}},
        },
    )
    async def create_album(  # type: ignore[override]
        request: SCreateAlbumRequest = Depends(SCreateAlbumRequest),
        service: BaseService = Depends(get_service),
        current_user: CurrentUser = Depends(get_current_user),
    ) -> SCreateAlbumResponse:
        logger.info("create_album API request")
        async with exception_handler():
            response = await service.create_album(
                user_id=current_user.id,
                title=request.title,
                description=request.description,
                tags=request.tags,
            )
        return SCreateAlbumResponse(id=response.id)

    @staticmethod
    @router_v1.put(
        path="/{album_id}",
        summary="Update an album",
        responses={
            status.HTTP_200_OK: {"model": SUpdateAlbumResponse},
            status.HTTP_403_FORBIDDEN: {"content": {"application/json": examples()[status.HTTP_403_FORBIDDEN]}},
            status.HTTP_404_NOT_FOUND: {"content": {"application/json": examples()[status.HTTP_404_NOT_FOUND]}},
        },
    )
    async def update_album(  # type: ignore[override]
        request: SUpdateAlbumRequest = Depends(SUpdateAlbumRequest),
        service: BaseService = Depends(get_service),
        current_user: CurrentUser = Depends(get_current_user),
    ) -> SUpdateAlbumResponse:
        logger.info("update_album API request")
        async with exception_handler():
            response = await service.update_album(
                album_id=request.id,
                user_id=current_user.id,
                title=request.title,
                description=request.description,
                artists_ids=request.artists_ids,
                tracks_ids=request.tracks_ids,
                tags=request.tags,
            )
        return SUpdateAlbumResponse(id=response.id)

    @staticmethod
    @router_v1.delete(
        path="/{album_id}",
        summary="Delete an album",
        responses={
            status.HTTP_204_NO_CONTENT: {"model": None},
            status.HTTP_403_FORBIDDEN: {"content": {"application/json": examples()[status.HTTP_403_FORBIDDEN]}},
            status.HTTP_404_NOT_FOUND: {"content": {"application/json": examples()[status.HTTP_404_NOT_FOUND]}},
        },
    )
    async def delete_album(  # type: ignore[override]
        request: SDeleteAlbumRequest = Depends(SDeleteAlbumRequest),
        service: BaseService = Depends(get_service),
        current_user: CurrentUser = Depends(get_current_user),
    ) -> None:
        logger.info("delete_album API request")
        async with exception_handler():
            await service.delete_album(
                album_id=request.album_id,
                user_id=current_user.id,
            )


def get_router() -> Router:
    return Router()
