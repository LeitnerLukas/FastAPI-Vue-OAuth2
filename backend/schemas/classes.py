from pydantic import BaseModel

class Base(BaseModel):
    class_id: str
    girl_count: int
    boy_count: int

class Create(BaseModel):
    class_id: str
    girl_count: int
    boy_count: int

class Update(BaseModel):
    girl_count: int
    boy_count: int
