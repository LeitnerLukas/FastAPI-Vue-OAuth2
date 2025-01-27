from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth.utils import get_password_hash
from models.db import UserModels
import schemas.user as user_schema


class UserCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def check_username (self, username: str) -> bool:
        valid_domain = "lr.htlweiz.at"
        if username.split('@')[-1] != valid_domain:
            return False
        return True
    
    async def get_user_by_username(self, username: str):
        stmt = select(UserModels).where(UserModels.username == username)
        result = await self.db_session.execute(stmt)
        user = result.scalars().first()
        return user

    async def get_users(self) -> List[user_schema.DB]:
        stmt = select(UserModels)
        result = await self.db_session.execute(stmt)
        users = result.scalars().all()
        return users

    async def create_user(self, user: user_schema.Create) -> user_schema.DB:
        if not await self.check_username(user.username):
            return None
        db_user = UserModels(
            username=user.username,
            name=user.name,
        )
        self.db_session.add(db_user)
        await self.db_session.commit()
        return db_user
    
    async def super_user_login(self, username: str, api_key: str):
        if api_key != "super_secret_key":
            return None
        db_user = await self.get_user_by_username(username)
        if db_user is not None:
            return None
        db_user = UserModels(
            username=username,
            request_permission=True,
        )

    async def update_user_login(self, username: str):
        db_user = await self.get_user_by_username(username)
        db_user.last_login = datetime.now()
        await self.db_session.refresh(db_user)
        return db_user

    async def update_birthday(self, username: str, birthday: datetime):
        stmt = (
            update(UserModels)
            .where(UserModels.username == username)
            .values(birthday=birthday)
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def update_password(self, username: str, password: str):
        stmt = (
            update(UserModels)
            .where(UserModels.username == username)
            .values(password=get_password_hash(password))
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def delete_user(self, username: str):
        stmt = delete(UserModels).where(UserModels.username == username)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
