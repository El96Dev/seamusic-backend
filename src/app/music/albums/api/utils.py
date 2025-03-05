from dataclasses import dataclass

# from src.domain.auth.users.core.service import BaseService
from src.domain.music.albums.api.schemas import BaseCurrentUser
from src.infrastructure.loggers import app as logger


@dataclass
class CurrentUser(BaseCurrentUser):
    id: int


async def get_current_user() -> CurrentUser:
    logger.info("get_current_user API utils request")
    return CurrentUser(id=1)
