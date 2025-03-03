from pydantic import BaseModel
from datetime import datetime
from crud.types import AcceptState
from typing import Optional

class NoteBase(BaseModel):
    event_state: AcceptState
    note: str
    activity_id: int

class NoteCreate(NoteBase):
    pass  

class NoteUpdate(BaseModel):
    event_state: Optional[AcceptState] = None
    note: Optional[str] = None