from fastapi import APIRouter, Depends
from typing import List

from crud.classes import ClassCRUD
import schemas.classes as class_schema
from crud.dependencies import get_classes_crud

router = APIRouter(prefix="/classes", tags=["classes"])

@router.get("", response_model=List[class_schema.Base])
async def get_classes(db: ClassCRUD = Depends(get_classes_crud)):
    return await db.get_classes()

@router.get("/{classId}", response_model=class_schema.Base)
async def get_class_by_id(classId: str, db: ClassCRUD = Depends(get_classes_crud)):
    return await db.get_class_by_id(classId)

@router.post("")
async def create_class(new_class: class_schema.Create, db: ClassCRUD = Depends(get_classes_crud)):
    await db.create_class(new_class)
    return new_class

@router.put("/{classId}")
async def update_class(classId: str, class_: class_schema.Update, db: ClassCRUD = Depends(get_classes_crud)):
    await db.update_class(classId, class_)
    return class_

@router.delete("/{classId}")
async def delete_class(classId: str, db: ClassCRUD = Depends(get_classes_crud)):
    await db.delete_class(classId)
    return {"message": "Class deleted successfully"}
