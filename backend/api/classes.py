from fastapi import APIRouter, Depends, HTTPException
from typing import List

from crud.classes import ClassCRUD
from crud.user import UserCRUD
import schemas.classes as class_schema
from crud.dependencies import get_classes_crud, get_user_crud

router = APIRouter(prefix="/classes", tags=["classes"])

@router.get("", response_model=List[class_schema.Base])
async def get_classes(token:str, db: ClassCRUD = Depends(get_classes_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await db.get_classes()

@router.get("/{classId}", response_model=class_schema.Base)
async def get_class_by_id(token:str, classId: str, db: ClassCRUD = Depends(get_classes_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await db.get_class_by_id(classId)

@router.post("")
async def create_class(token:str, new_class: class_schema.Create, db: ClassCRUD = Depends(get_classes_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    await db.create_class(new_class)
    return new_class

@router.put("/{classId}")
async def update_class(token:str, classId: str, class_: class_schema.Update, db: ClassCRUD = Depends(get_classes_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    await db.update_class(classId, class_)
    return class_

@router.delete("/{classId}")
async def delete_class(token:str, classId: str, db: ClassCRUD = Depends(get_classes_crud), user_db: UserCRUD = Depends(get_user_crud)):
    current = await user_db.get_current_user(token)
    if not current.username:
        raise HTTPException(status_code=403, detail="Forbidden")
    await db.delete_class(classId)
    return {"message": "Class deleted successfully"}
