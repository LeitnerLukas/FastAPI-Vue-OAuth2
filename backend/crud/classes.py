from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from typing import List

from models.db import Classes
import schemas.classes as class_schema

class ClassCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_classes(self) -> List[class_schema.Base]:
        stmt = select(Classes).options(
            joinedload(Classes.activities),
        )
        result = await self.db_session.execute(stmt)
        classes = result.unique().scalars().all()
        return classes
    
    async def get_class_by_id(self, class_id: str):
        stmt = select(Classes).options(
            joinedload(Classes.activities),
        ).filter_by(class_id=class_id)
        result = await self.db_session.execute(stmt)
        classes = result.scalars().first()
        return classes
    
    async def create_class(self, class_: class_schema.Create) -> class_schema.Base:
        db_class = Classes(
            class_id=class_.class_id,
            girl_count=class_.girl_count,
            boy_count=class_.boy_count,
        )
        self.db_session.add(db_class)
        await self.db_session.commit()
        return db_class

    async def update_class(self, class_id: str, class_: class_schema.Update):
        stmt_classes = (
            update(Classes)
            .where(Classes.class_id == class_id)
            .values(girl_count=class_.girl_count,
                    boy_count=class_.boy_count,
            )
        )
        stmt_classes.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt_classes)
        await self.db_session.commit()

    async def delete_class(self, class_id: str):
        stmt = delete(Classes).where(Classes.class_id == class_id)
        await self.db_session.execute(stmt)
