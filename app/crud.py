from sqlalchemy.orm import Session
from app import models, schemas
from app.cache import get_cache, set_cache, delete_cache

def create_match(db: Session, match_in: schemas.MatchCreate):
    db_match = models.Match(**match_in.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    # Invalida cache general (listado) si existiera
    delete_cache("matches:all")
    return db_match

def get_match(db: Session, match_id: int):
    cache_key = f"match:{match_id}"
    cached = get_cache(cache_key)
    if cached:
        print(f"[Cache HIT] {cache_key}")
        return schemas.MatchOut(**cached)

    print(f"[Cache MISS] {cache_key}")
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if match:
        set_cache(cache_key, schemas.MatchOut.from_orm(match).dict())
    return match

def list_matches(db: Session, skip: int = 0, limit: int = 100, referee_id: int = None):
    cache_key = f"matches:{referee_id or 'all'}:{skip}:{limit}"
    cached = get_cache(cache_key)
    if cached:
        print(f"[Cache HIT] {cache_key}")
        return [schemas.MatchOut(**m) for m in cached]

    print(f"[Cache MISS] {cache_key}")
    query = db.query(models.Match)
    if referee_id:
        query = query.filter(models.Match.referee_id == referee_id)
    matches = query.offset(skip).limit(limit).all()

    set_cache(cache_key, [schemas.MatchOut.from_orm(m).dict() for m in matches])
    return matches

def update_match(db: Session, match_id: int, match_in: schemas.MatchUpdate):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        return None
    for field, value in match_in.dict(exclude_unset=True).items():
        setattr(match, field, value)
    db.commit()
    db.refresh(match)
    # Invalida cache del partido y del listado
    delete_cache(f"match:{match_id}")
    delete_cache("matches:all")
    return match

def delete_match(db: Session, match_id: int):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        return None
    db.delete(match)
    db.commit()
    # Invalida cache correspondiente
    delete_cache(f"match:{match_id}")
    delete_cache("matches:all")
    return match
