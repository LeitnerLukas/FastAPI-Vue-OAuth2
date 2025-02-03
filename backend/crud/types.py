from enum import Enum

class AcceptState(Enum):
    APPROVED = "approved"
    SUPER_APPROVED = "super_approved"
    REQUESTED = "requested"
    DENIED = "denied"