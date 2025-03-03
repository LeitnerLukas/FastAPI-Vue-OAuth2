from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import Depends, status, HTTPException


from models.db import Roles
import schemas.roles as roles_schema
from models.db import user_role

class RolesCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_roles(self):
        stmt = select(Roles)
        result = await self.db_session.execute(stmt)
        roles = result.unique().scalars().all()
        return roles
    
    async def get_role_by_name(self, name: str) -> roles_schema.DB:
        stmt = select(Roles).where(Roles.name == name)
        result = await self.db_session.execute(stmt)
        role = result.scalars().first()
        return role
    
    async def get_roles_by_user(self, username: str):
        stmt = select(Roles).join(user_role, Roles.name == user_role.c.role_name).where(user_role.c.username == username)
        result = await self.db_session.execute(stmt)
        roles = result.scalars().all()
        return roles

    async def create_role(self, role: roles_schema.Create):
        db_role = Roles(
            name=role.name,
            approvement_permission=role.approvement_permission,
            super_approvement_permission=role.super_approvement_permission,
            request_permission=role.request_permission,
            change_permission=role.change_permission
        )
        self.db_session.add(db_role)
        await self.db_session.commit()
        return db_role
    
    async def get_approvement_permission(self, username: str):
        stmt = select(Roles).join(user_role, Roles.name == user_role.c.role_name).where(user_role.c.username == username, Roles.approvement_permission == True)
        result = await self.db_session.execute(stmt)
        role = result.scalars().first()
        return role is not None
    
    async def get_super_approvement_permission(self, username: str):
        stmt = select(Roles).join(user_role, Roles.name == user_role.c.role_name).where(user_role.c.username == username, Roles.super_approvement_permission == True)
        result = await self.db_session.execute(stmt)
        role = result.scalars().first()
        return role is not None
    
    async def get_request_permission(self, username: str):
        stmt = select(Roles).join(user_role, Roles.name == user_role.c.role_name).where(user_role.c.username == username, Roles.request_permission == True)
        result = await self.db_session.execute(stmt)
        role = result.scalars().first()
        return role is not None
    
    async def get_change_permission(self, username: str):
        stmt = select(Roles).join(user_role, Roles.name == user_role.c.role_name).where(user_role.c.username == username, Roles.change_permission == True)
        result = await self.db_session.execute(stmt)
        role = result.scalars().first()
        return role is not None
    
    async def give_user_role(self, role: str, username: str):
        stmt = user_role.insert().values(username=username, role_name=role)
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    async def remove_user_role(self, role: str, username: str):
        stmt = delete(user_role).where(user_role.c.username == username, user_role.c.role_name == role)
        await self.db_session.execute(stmt)
        await self.db_session.commit()
    
    async def update_role(self, role: roles_schema.Create):
        db_role = await self.get_role_by_name(role.name)
        db_role.approvement_permission = role.approvement_permission
        db_role.super_approvement_permission = role.super_approvement_permission
        db_role.request_permission = role.request_permission
        db_role.change_permission = role.change_permission
        await self.db_session.commit()
        await self.db_session.refresh(db_role)
        return db_role

    async def delete_role(self, name: str):
        stmt = delete(Roles).where(Roles.name == name)
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        return None