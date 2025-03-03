from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.db import Activities
from crud.activities import ActivityCRUD
from crud.user import UserCRUD
from crud.roles import RolesCRUD
from crud.dependencies import get_activities_crud, get_user_crud, get_roles_crud
from crud.types import AcceptState
from schemas.activities import Base

router = APIRouter(prefix="/approve", tags=["approve"])


@router.post("/activities/{activity_id}/approve")
async def approve_activity(token:str, activity_id: int, activity_db: ActivityCRUD = Depends(get_activities_crud), user_db: UserCRUD = Depends(get_user_crud), roles_db: RolesCRUD = Depends(get_roles_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    check_permission = await roles_db.get_approvement_permission(current.username)
    if not check_permission:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, no permission."
        )
    activity: Base  = await activity_db.get_activity_by_id(activity_id)
    print(activity.state)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    if activity.state != AcceptState.REQUESTED:
        raise HTTPException(status_code=400, detail="Activity must be in 'requested' state to approve")
    
    activity.state = AcceptState.APPROVED
    await activity_db.update_activity(activity_id=activity_id, activity=activity)
    return {"message": "Activity approved", "activity": activity}


@router.post("/activities/{activity_id}/super_approve")
async def super_approve_activity(token:str, activity_id: int, activity_db: ActivityCRUD = Depends(get_activities_crud), user_db: UserCRUD = Depends(get_user_crud), roles_db: RolesCRUD = Depends(get_roles_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    check_permission = await roles_db.get_super_approvement_permission(current.username)
    if not check_permission:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, no permission."
        )
    activity: Base = await activity_db.get_activity_by_id(activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    print(activity.state)
    if activity.state != AcceptState.APPROVED:
        raise HTTPException(status_code=400, detail="Activity must be 'approved' before super approval")
    
    activity.state = AcceptState.SUPER_APPROVED
    await activity_db.update_activity(activity_id=activity_id, activity=activity)
    return {"message": "Activity super approved", "activity": activity}


@router.post("/activities/{activity_id}/reject")
async def reject_activity(token:str, activity_id: int, activity_db: ActivityCRUD = Depends(get_activities_crud), user_db: UserCRUD = Depends(get_user_crud), roles_db: RolesCRUD = Depends(get_roles_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    check_permission = await roles_db.get_approvement_permission(current.username)
    if not check_permission:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, no permission."
        )
    
    activity: Base = await activity_db.get_activity_by_id(activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity.state = AcceptState.DENIED
    await activity_db.update_activity(activity_id=activity_id, activity=activity)
    return {"message": "Activity rejected", "activity": activity}