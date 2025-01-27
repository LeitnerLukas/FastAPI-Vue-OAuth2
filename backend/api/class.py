from fastapi import APIRouter
from typing import List

from crud.classes import ClassCRUD
import schemas.classes as class_schema

router = APIRouter(prefix="/classes", tags=["classes"])

@router.get("", response_model=List[class_schema.Base])
async def get_classes(db: ClassCRUD):
    return await db.get_classes()

@router.get("/{classId}", response=class_schema.Base)
async def get_class_by_id(classId: int, db: ClassCRUD):
    return await db.get_class_by_id(classId)

@router.post("")
async def create_class(new_class: class_schema.Create, db: ClassCRUD):
    return await db.create_class(new_class)

@router.put("")
async def update_class(classId: int, class_: class_schema.Update, db: ClassCRUD):
    return await db.update_class(classId, class_)

@router.delete("")
async def delete_class(classId: int, db: ClassCRUD):
    return await db.delete_class(classId)
