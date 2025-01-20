from pydantic import BaseModel
from enum import Enum

class EventState(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ActivityApprovalRequest(BaseModel):
    userid: int
    event_state: EventState  
    note: str = None  


