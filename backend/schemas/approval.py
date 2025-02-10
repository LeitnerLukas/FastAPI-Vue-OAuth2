from pydantic import BaseModel
from enum import Enum
from crud.types import AcceptState

class ActivityApprovalRequest(BaseModel):
    userid: int
    event_state: AcceptState  
    note: str = None  


