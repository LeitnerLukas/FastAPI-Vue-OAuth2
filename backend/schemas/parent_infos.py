from pydantic import BaseModel

class Base(BaseModel):
    parent_info_id: int
    activity_id: int
    text: str

class Create(BaseModel):
    activity_id: int
    text: str

class Update(BaseModel):
    activity_id: int
    text: str
