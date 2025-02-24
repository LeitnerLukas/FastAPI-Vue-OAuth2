from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import schemas.user as user_schema
import schemas.classes as class_schema
import schemas.parent_infos as parent_info_schema

class Base(BaseModel):
    activity_id: int
    location: str
    description: str
    curriculum_reference: str
    cost: int
    transfer_cost: int
    start_time: datetime
    end_time: datetime
    sga_approved: bool
    create_time: datetime
    last_update: datetime
    users: List[user_schema.DB]
    classes: List[class_schema.Base]
    parent_infos: List[parent_info_schema.Base]

    class Config:
        orm_mode = True

class Create(BaseModel):
    location: str
    description: str
    curriculum_reference: str
    cost: int
    transfer_cost: int
    start_time: datetime
    end_time: datetime
    sga_approved: bool

class Update(BaseModel):
    location: Optional[str]
    description: Optional[str]
    curriculum_reference: Optional[str]
    cost: Optional[int]
    transfer_cost: Optional[int]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    last_update: Optional[datetime] = datetime.now()
    sga_approved: bool
