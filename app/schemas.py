# schemas.py
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from enum import Enum

class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    FINISHED = "finished"
    CANCELED = "canceled"

class MatchBase(BaseModel):
    team_a: str
    team_b: str
    referee_id: int
    scheduled_at: datetime
    location: Optional[str] = None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(BaseModel):
    team_a: Optional[str] = None
    team_b: Optional[str] = None
    referee_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None
    location: Optional[str] = None
    status: Optional[MatchStatus] = None
    result: Optional[Any] = None

class MatchOut(MatchBase):
    id: int
    status: MatchStatus
    result: Optional[Any]
    created_at: datetime
    updated_at: Optional[datetime]

    # Pydantic v2
    model_config = {
        "from_attributes": True
    }
