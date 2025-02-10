from fastapi import APIRouter, HTTPException
import crud.user as user_crud
from crud.user import UserCRUD
from crud.dependencies import get_user_crud
from fastapi import Depends


router = APIRouter()

@router.get("/test")
async def test(token: str, db: UserCRUD = Depends(get_user_crud)):
    result = await db.get_current_user(token=token)
    return result