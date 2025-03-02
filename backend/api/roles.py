from fastapi import APIRouter, HTTPException
from crud.roles import RolesCRUD
from crud.user import UserCRUD
from crud.dependencies import get_roles_crud, get_user_crud
from fastapi import Depends, status
from typing import List
import schemas.roles as roles_schema

router = APIRouter(prefix="/roles", tags=["roles"])
router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/roles", response_model=List[roles_schema.DB], status_code=200)
async def get_roles(token:str, db: RolesCRUD = Depends(get_roles_crud), user_db: UserCRUD = Depends(get_user_crud)):
    check = await user_db.get_current_user(token)
    if not check.username:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    
    result = await db.get_roles()
    return result

@router.get("/role/{name}", response_model=roles_schema.DB, status_code=200)
async def get_role_by_name(token:str, name: str, db: RolesCRUD = Depends(get_roles_crud), user_db: UserCRUD = Depends(get_user_crud)):
    check = await user_db.get_current_user(token)
    if not check.username:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    result = await db.get_role_by_name(name)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )
    return result

@router.get("/roles/{username}", response_model=List[roles_schema.DB], status_code=200)
async def get_roles_by_user(token:str, username: str, db: RolesCRUD = Depends(get_roles_crud), user_db: UserCRUD = Depends(get_user_crud)):
    check = await user_db.get_current_user(token)
    if not check.username:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    result = await db.get_roles_by_user(username)
    return result

@router.post("/role", status_code=201)
async def create_role(token:str, role: roles_schema.Create, db: RolesCRUD = Depends(get_roles_crud), user_db: UserCRUD = Depends(get_user_crud)):
    check = await user_db.get_current_user(token)
    if not check.username:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    role_check = await db.get_role_by_name(role.name)
    if role_check:
        raise HTTPException(
            status_code=400,
            detail="Role already exists"
        )
    check_permission = await db.get_change_permission(check.username)
    if not check_permission:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, no permission."
        )
    await db.create_role(role)
    return status.HTTP_201_CREATED

@router.post("/role/user", status_code=200)
async def give_user_role(token:str, role: str, username: str, db: RolesCRUD = Depends(get_roles_crud), user_db: UserCRUD = Depends(get_user_crud)):
    check = await user_db.get_current_user(token)
    if not check.username:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    role_check = await db.get_role_by_name(role)
    if not role_check:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )
    user_check = await user_db.get_user_by_username(username)
    if not user_check:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    check_permission = await db.get_change_permission(check.username)
    if not check_permission:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, no permission."
        )
    await db.give_user_role(role, username)
    return status.HTTP_200_OK

@router.delete("/role/user", status_code=200)
async def remove_user_role(token:str, role: str, username: str, db: RolesCRUD = Depends(get_roles_crud), user_db: UserCRUD = Depends(get_user_crud)):
    check = await user_db.get_current_user(token)
    if not check.username:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    role_check = await db.get_role_by_name(role)
    if not role_check:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )
    user_check = await user_db.get_user_by_username(username)
    if not user_check:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    check_permission = await db.get_change_permission(check.username)
    if not check_permission:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, no permission."
        )
    await db.remove_user_role(role, username)
    return status.HTTP_200_OK