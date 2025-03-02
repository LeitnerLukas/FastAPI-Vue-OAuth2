from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from typing import List

from models.db import ParentInfos
import schemas.parent_infos as parent_schema

class ParentInfosCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_parent_infos(self) -> List[parent_schema.Base]:
        stmt = select(ParentInfos).options(
            joinedload(ParentInfos.activity),
        )
        result = await self.db_session.execute(stmt)
        parent_infos = result.unique().scalars().all()
        return parent_infos

    async def get_parent_info_by_id(self, parent_info_id: int) -> parent_schema.Base:
        stmt = select(ParentInfos).options(
            joinedload(ParentInfos.activity),
        ).filter_by(parent_info_id=parent_info_id)
        result = await self.db_session.execute(stmt)
        parent_info = result.scalars().first()
        return parent_info

    async def create_parent_info(self, parent_info: parent_schema.Create) -> parent_schema.Base:
        db_parent_info = ParentInfos(
            activity_id=parent_info.activity_id,
            text=parent_info.text,
        )
        self.db_session.add(db_parent_info)
        await self.db_session.commit()
        return db_parent_info
    
    async def update_parent_info(self, parent_info_id: int, parent_info: parent_schema.Update):
        stmt_parent_infos = (
            update(ParentInfos)
            .where(ParentInfos.parent_info_id == parent_info_id)
            .values(activity_id=parent_info.activity_id,
                    text=parent_info.text,
            )
        )
        stmt_parent_infos.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt_parent_infos)
        await self.db_session.commit()

    async def delete_parent_info(self, parent_info_id: int):
        stmt = delete(ParentInfos).where(ParentInfos.parent_info_id == parent_info_id)
        await self.db_session.execute(stmt)
