from fastapi import APIRouter, Depends
from typing import List

from crud.parent_infos import ParentInfosCRUD
from crud.user import UserCRUD
import schemas.parent_infos as parent_schema
from crud.dependencies import get_parent_infos_crud, get_user_crud
from fastapi import HTTPException

router = APIRouter(prefix="/parent_infos", tags=["parent_infos"])

@router.get("", response_model=List[parent_schema.Base])
async def get_parent_infos(token:str, db: ParentInfosCRUD = Depends(get_parent_infos_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await db.get_parent_infos()

@router.get("/{parentInfoId}", response_model=parent_schema.Base)
async def get_parent_info_by_id(token:str, parentInfoId: int, db: ParentInfosCRUD = Depends(get_parent_infos_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await db.get_parent_info_by_id(parentInfoId)

@router.post("")
async def create_parent_info(token:str, new_parent_info: parent_schema.Create, db: ParentInfosCRUD = Depends(get_parent_infos_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    await db.create_parent_info(new_parent_info)
    return new_parent_info

@router.put("/{parentInfoId}")
async def update_parent_info(token:str, parentInfoId: int, parent_info: parent_schema.Update, db: ParentInfosCRUD = Depends(get_parent_infos_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await db.update_parent_info(parentInfoId, parent_info)

@router.delete("/{parentInfoId}")
async def delete_parent_info(token:str, parentInfoId: int, db: ParentInfosCRUD = Depends(get_parent_infos_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await db.delete_parent_info(parentInfoId)
