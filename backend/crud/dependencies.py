from typing import Generator

from database.config import async_session
from crud.user import UserCRUD
from enum import Enum

class AcceptState(Enum):
    APPROVED = "approved"
    SUPER_APPROVED = "super_approved"
    REQUESTED = "requested"
    DENIED = "denied"

async def get_db() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield session


async def get_user_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield UserCRUD(session)
