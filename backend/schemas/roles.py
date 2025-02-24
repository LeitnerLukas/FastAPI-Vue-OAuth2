from pydantic import BaseModel

# User Schema

class DB(BaseModel):
    name: str
    approvement_permission: bool
    super_approvement_permission: bool
    request_permission: bool
    change_permission: bool

class Create(BaseModel):
    name: str
    approvement_permission: bool
    super_approvement_permission: bool
    request_permission: bool
    change_permission: bool
