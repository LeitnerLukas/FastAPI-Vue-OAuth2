from datetime import datetime

from pydantic import BaseModel

# User Schema


class DB(BaseModel):
    username: str
    name: str
    create_time: datetime
    last_login: datetime

class Create(BaseModel):
    username: str
    name: str