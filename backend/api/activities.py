from fastapi import APIRouter, Depends, HTTPException
from typing import List

from crud.activities import ActivityCRUD
from crud.user import UserCRUD
from crud.roles import RolesCRUD
import schemas.activities as activities_schema
from crud.dependencies import get_activities_crud, get_user_crud, get_roles_crud

router = APIRouter(prefix="/activities", tags=["activities"])

@router.get("", response_model=List[activities_schema.Base])
async def get_activities(token:str, db: ActivityCRUD = Depends(get_activities_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    activities = await db.get_activities()
    return activities

@router.get("/{activityId}", response_model=activities_schema.Base)
async def get_activity_by_id(token:str, activityId: int, db: ActivityCRUD = Depends(get_activities_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    activity = await db.get_activity_by_id(activityId)
    return activity

@router.post("")
async def create_activity(token:str, new_activity: activities_schema.Create, roles_db: RolesCRUD = Depends(get_roles_crud), db: ActivityCRUD = Depends(get_activities_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    check_permission = await roles_db.get_request_permission(current.username)
    if not check_permission:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, no permission."
        )
    await db.create_activity(new_activity)
    return new_activity

@router.put("/{activityId}") 
async def update_activity(token:str, activityId: int, activity: activities_schema.Update, roles_db: RolesCRUD = Depends(get_roles_crud), db: ActivityCRUD = Depends(get_activities_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    check_permission = await roles_db.get_request_permission(current.username)
    if not check_permission:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, no permission."
        )
    await db.update_activity(activityId, activity)
    return activity

@router.delete("/{activityId}")
async def delete_activity(token:str, activityId: int, roles_db: RolesCRUD = Depends(get_roles_crud), db: ActivityCRUD = Depends(get_activities_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    check_permission = await roles_db.get_request_permission(current.username)
    if not check_permission:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, no permission."
        )
    await db.delete_activity(activityId)
    return {"message": "Activity deleted successfully"}
