from fastapi import APIRouter, Depends
from typing import List

from crud.parent_infos import ParentInfosCRUD
import schemas.parent_infos as parent_schema
from crud.dependencies import get_parent_infos_crud

router = APIRouter(prefix="/parent_infos", tags=["parent_infos"])

@router.get("/parent_infos", response_model=List[parent_schema.Base])
async def get_parent_infos(db: ParentInfosCRUD = Depends(get_parent_infos_crud)):
    return await db.get_parent_infos()

@router.get("/parent_infos/{parentInfoId}", response_model=parent_schema.Base)
async def get_parent_info_by_id(parentInfoId: int, db: ParentInfosCRUD = Depends(get_parent_infos_crud)):
    return await db.get_parent_info_by_id(parentInfoId)

@router.post("/parent_infos")
async def create_parent_info(new_parent_info: parent_schema.Create, db: ParentInfosCRUD = Depends(get_parent_infos_crud)):
    await db.create_parent_info(new_parent_info)
    return new_parent_info

@router.put("/parent_infos")
async def update_parent_info(parentInfoId: int, parent_info: parent_schema.Update, db: ParentInfosCRUD = Depends(get_parent_infos_crud)):
    return await db.update_parent_info(parentInfoId, parent_info)

@router.delete("/parent_infos")
async def delete_parent_info(parentInfoId: int, db: ParentInfosCRUD = Depends(get_parent_infos_crud)):
    return await db.delete_parent_info(parentInfoId)
