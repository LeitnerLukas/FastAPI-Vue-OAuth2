from fastapi import APIRouter
from typing import List

from crud.parent_infos import ParentInfosCRUD
import schemas.parent_infos as parent_schema

router = APIRouter(prefix="/parent_infos", tags=["parent_infos"])

@router.get("", response_model=List[parent_schema.Base])
async def get_parent_infos(db: ParentInfosCRUD):
    return await db.get_parent_infos()

@router.get("/{parentInfoId}", response=parent_schema.Base)
async def get_parent_info_by_id(parentInfoId: int, db: ParentInfosCRUD):
    return await db.get_parent_info_by_id(parentInfoId)

@router.post("")
async def create_parent_info(new_parent_info: parent_schema.Create, db: ParentInfosCRUD):
    return await db.create_parent_info(new_parent_info)

@router.put("")
async def update_parent_info(parentInfoId: int, parent_info: parent_schema.Update, db: ParentInfosCRUD):
    return await db.update_parent_info(parentInfoId, parent_info)

@router.delete("")
async def delete_parent_info(parentInfoId: int, db: ParentInfosCRUD):
    return await db.delete_parent_info(parentInfoId)
