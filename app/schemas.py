# schemas.py
from pydantic import BaseModel, Field
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
    team_a: Optional[str]
    team_b: Optional[str]
    referee_id: Optional[int]
    scheduled_at: Optional[datetime]
    location: Optional[str]
    status: Optional[MatchStatus]
    result: Optional[Any]

class MatchOut(MatchBase):
    id: int
    status: MatchStatus
    result: Optional[Any]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
      
