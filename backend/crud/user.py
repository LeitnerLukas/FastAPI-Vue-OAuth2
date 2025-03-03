from datetime import datetime

from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from schemas.token import TokenData
from models.db import user_role

from auth.utils import get_password_hash
from models.db import UserModels
import schemas.user as user_schema
from passlib.context import CryptContext

from os import getenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = str(getenv("SECRET_KEY"))
ALGORITHM = "HS256"

class UserCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def check_username (self, username: str) -> bool:
        valid_domain = "lr.htlweiz.at"
        if username.split('@')[-1] != valid_domain:
            return False
        return True
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
            username: str = payload["username"]
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user: user_schema.DB = await self.get_user_by_username(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    
    async def get_user_by_username(self, username: str) -> user_schema.DB:
        stmt = select(UserModels).where(UserModels.username == username)
        result = await self.db_session.execute(stmt)
        user = result.scalars().first()
        return user

    async def get_users(self) -> List[user_schema.DB]:
        stmt = select(UserModels)
        result = await self.db_session.execute(stmt)
        users = result.scalars().all()
        return users

    async def create_user(self, user: user_schema.DB) -> user_schema.DB:
        #check = await self.check_username(user.username)
        #if not check:
            #raise HTTPException(
                #status_code=400,
                #detail="Invalid domain"
            #)
        stmt = (
            insert(UserModels)
            .values(username=user.username, name=user.name)
        )
        stmt2 = None
        if user.username == "superuser":
            stmt2 = insert(user_role).values(username=user.username, role_name="superuser")
        else:   
            stmt2 = insert(user_role).values(username=user.username, role_name="teacher")
        stmt.execution_options(synchronize_session="fetch")
        stmt2.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
        await self.db_session.execute(stmt2)
        await self.db_session.commit()
        return user

    async def update_user_login(self, username: str):
        db_user = await self.get_user_by_username(username)
        db_user.last_login = datetime.now()
        await self.db_session.commit()

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
