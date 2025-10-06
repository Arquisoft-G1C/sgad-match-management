# crud.py
from sqlalchemy.orm import Session
from app.models import Match, MatchStatus
from app import schemas
from typing import List, Optional

def create_match(db: Session, match_in: schemas.MatchCreate) -> Match:
    db_match = Match(
        team_a=match_in.team_a,
        team_b=match_in.team_b,
        referee_id=match_in.referee_id,
        scheduled_at=match_in.scheduled_at,
        location=match_in.location,
        status=MatchStatus.SCHEDULED
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def get_match(db: Session, match_id: int) -> Optional[Match]:
    return db.query(Match).filter(Match.id == match_id).first()

def list_matches(db: Session, skip: int = 0, limit: int = 100, referee_id: Optional[int] = None):
    q = db.query(Match)
    if referee_id is not None:
        q = q.filter(Match.referee_id == referee_id)
    return q.order_by(Match.scheduled_at).offset(skip).limit(limit).all()

def update_match(db: Session, match_id: int, match_in: schemas.MatchUpdate):
    db_obj = get_match(db, match_id)
    if not db_obj:
        return None
    for field, value in match_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_match(db: Session, match_id: int):
    obj = get_match(db, match_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
  
