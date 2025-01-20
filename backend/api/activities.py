from fastapi import APIRouter
from typing import List

from crud.activities import ActivityCRUD
import schemas.activities as activities_schema

router = APIRouter(prefix="/activities", tags=["activities"])

@router.get("", response_model=List[activities_schema.Base])
async def get_activities(db: ActivityCRUD):
    return await db.get_activities()

@router.get("/{activityId}", response=activities_schema.Base)
async def get_activity_by_id(activityId: int, db: ActivityCRUD):
    return await db.get_activity_by_id(activityId)

@router.post("")
async def create_activity(new_activity: activities_schema.Create, db: ActivityCRUD):
    return await db.create_activity(new_activity)

@router.put("", deprecated=True)
async def update_activity(activityId: int, activity: activities_schema.Update, db: ActivityCRUD):
    return await db.update_activity(activityId, activity)

@router.delete("", deprecated=True)
async def delete_activity(activityId: int, db: ActivityCRUD):
    return await db.delete_activity(activityId)
