from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from typing import List

from models.db import Activities
import schemas.activities as activity_schema

class ActivityCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session
    
    async def get_activities(self) -> List[activity_schema.Base]:
        stmt = select(Activities).options(
            joinedload(Activities.users),
            joinedload(Activities.classes),
            joinedload(Activities.parent_infos),
            # joinedload(Activities.notes),
        )
        result = await self.db_session.execute(stmt)
        activities = result.unique().scalars().all()
        return activities
    
    async def get_activity_by_id(self, activity_id: int) -> activity_schema.Base:
        stmt = select(Activities).options(
            joinedload(Activities.users),
            joinedload(Activities.classes),
            joinedload(Activities.parent_infos),
            # joinedload(Activities.notes),
        ).filter_by(activity_id=activity_id)
        result = await self.db_session.execute(stmt)
        activities = result.scalars().first()
        return activities
    
    async def create_activity(self, activity: activity_schema.Create) -> activity_schema.Base:
        db_activity = Activities(
            location=activity.location,
            description=activity.description,
            curriculum_reference=activity.curriculum_reference,
            cost=activity.cost,
            transfer_cost=activity.transfer_cost,
            start_time=activity.start_time,
            end_time=activity.end_time,
        )
        self.db_session.add(db_activity)
        await self.db_session.commit()
        return db_activity
    
    async def update_activity(self, activity_id: int, activity: activity_schema.Update):
        stmt_activities = (
            update(Activities)
            .where(Activities.activity_id == activity_id)
            .values(location=activity.location,
                description=activity.description,
                curriculum_reference=activity.curriculum_reference,
                cost=activity.cost,
                transfer_cost=activity.transfer_cost,
                start_time=activity.start_time,
                end_time=activity.end_time,
                last_update=activity.last_update
            )
        )
        stmt_activities.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt_activities)
        await self.db_session.commit()

    async def delete_activity(self, activity_id: int):
        stmt = delete(Activities).where(Activities.activity_id == activity_id)
        await self.db_session.execute(stmt)
