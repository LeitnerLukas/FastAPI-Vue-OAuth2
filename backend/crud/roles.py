from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import Depends, status, HTTPException


from models.db import Roles
import schemas.roles as roles_schema

from os import getenv

class RolesCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_roles(self):
        stmt = select(Roles)
        result = await self.db_session.execute(stmt)
        roles = result.scalars().all()
        return roles
    
    async def get_role_by_name(self, name: str) -> roles_schema.DB:
        stmt = select(Roles).where(Roles.name == name)
        result = await self.db_session.execute(stmt)
        role = result.scalars().first()
        return role
    
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