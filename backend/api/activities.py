from fastapi import APIRouter, Depends
from typing import List

from crud.activities import ActivityCRUD
import schemas.activities as activities_schema
from crud.dependencies import get_activities_crud

router = APIRouter(prefix="/activities", tags=["activities"])

@router.get("/activities", response_model=List[activities_schema.Base])
async def get_activities(db: ActivityCRUD = Depends(get_activities_crud)):
    return await db.get_activities()

@router.get("/activities/{activityId}", response_model=activities_schema.Base)
async def get_activity_by_id(activityId: int, db: ActivityCRUD = Depends(get_activities_crud)):
    return await db.get_activity_by_id(activityId)

@router.post("/activities")
async def create_activity(new_activity: activities_schema.Create, db: ActivityCRUD = Depends(get_activities_crud)):
    await db.create_activity(new_activity)
    return new_activity

@router.put("/activities")
async def update_activity(activityId: int, activity: activities_schema.Update, db: ActivityCRUD = Depends(get_activities_crud)):
    await db.update_activity(activityId, activity)
    return activity

@router.delete("/activities")
async def delete_activity(activityId: int, db: ActivityCRUD = Depends(get_activities_crud)):
    await db.delete_activity(activityId)
    return {"message": "Activity deleted successfully"}
