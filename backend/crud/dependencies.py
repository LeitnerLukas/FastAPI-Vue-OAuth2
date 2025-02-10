from typing import Generator

from database.config import async_session
from crud.user import UserCRUD
from crud.activities import ActivityCRUD
from crud.classes import ClassCRUD
from crud.parent_infos import ParentInfosCRUD


async def get_db() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield session


async def get_user_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield UserCRUD(session)

async def get_activities_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield ActivityCRUD(session)

async def get_classes_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield ClassCRUD(session)

async def get_parent_infos_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield ParentInfosCRUD(session)
