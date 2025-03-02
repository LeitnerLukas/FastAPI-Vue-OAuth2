from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from auth.action import get_current_user
from crud.user import UserCRUD
from crud.roles import RolesCRUD
from crud.dependencies import get_user_crud, get_roles_crud
import schemas.user as user_schema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[user_schema.DB])
async def get_users(token:str, db: UserCRUD = Depends(get_user_crud), roles_db: RolesCRUD = Depends(get_roles_crud)):
    current = await db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await db.get_users()

@router.get("/me")
async def get_me(token:str, db: UserCRUD = Depends(get_user_crud)):
    user = await db.get_current_user(token)
    return user

@router.get("/{username}", response_model=user_schema.DB)
async def get_user_by_username(token:str, username: str, db: UserCRUD = Depends(get_user_crud)):
    current = await db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    user = await db.get_user_by_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("")
async def login(
    new_user: user_schema.Create, db: UserCRUD = Depends(get_user_crud)
):
    return "depricated"
    db_user = await db.get_user_by_username(username=new_user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="Username already registered")
    await db.create_user(new_user)
    return status.HTTP_201_CREATED



