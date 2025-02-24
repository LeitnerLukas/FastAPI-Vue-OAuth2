from fastapi import APIRouter, HTTPException
from crud.roles import RolesCRUD
from crud.user import UserCRUD
from crud.dependencies import get_roles_crud
from fastapi import Depends
from typing import List
import schemas.roles as roles_schema

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/roles", response_model=List[roles_schema.DB], status_code=200)
async def get_roles(db: RolesCRUD = Depends(get_roles_crud)):
    result = await db.get_roles()
    return result

@router.get("/role/{name}", response_model=roles_schema.DB, status_code=200)
async def get_role_by_name(name: str, db: RolesCRUD = Depends(get_roles_crud)):
    result = await db.get_role_by_name(name)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )
    return result

@router.post("/role", status_code=201)
async def create_role(role: roles_schema.Create, db: RolesCRUD = Depends(get_roles_crud)):
    role_check = await db.get_role_by_name(role.name)
    if role_check:
        raise HTTPException(
            status_code=400,
            detail="Role already exists"
        )
    await db.create_role(role)