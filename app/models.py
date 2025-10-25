# models.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import enum

class MatchStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    FINISHED = "finished"
    CANCELED = "canceled"

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    team_a = Column(String, nullable=False)
    team_b = Column(String, nullable=False)
    referee_id = Column(Integer, nullable=False, index=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    location = Column(String, nullable=True)
    status = Column(Enum(MatchStatus), default=MatchStatus.SCHEDULED)
    result = Column(JSON, nullable=True)  # e.g. {"score_a": 1, "score_b": 2}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
  
