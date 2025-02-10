from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Base(BaseModel):
    activity_id: int
    location: str
    description: str
    curriculum_reference: str
    cost: int
    transfer_cost: int
    start_time: str
    end_time: str
    sga_approved: bool
    create_time: str
    last_update: str

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
