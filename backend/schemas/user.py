from datetime import date

from pydantic import BaseModel

# User Schema


class DB(BaseModel):
    username: str
    name: str
    roles: list[str]
    approvement_permission: bool
    super_approvement_permission: bool
    request_permission: bool
    change_permission: bool

