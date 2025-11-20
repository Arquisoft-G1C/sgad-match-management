from sqlalchemy.orm import Session
from app import models, schemas
from app.cache import get_cache, set_cache, delete_cache

def create_match(db: Session, match_in: schemas.MatchCreate):
    db_match = models.Match(**match_in.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)

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
        match_out = schemas.MatchOut.model_validate(match).model_dump()
        set_cache(cache_key, match_out)

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

    set_cache(
        cache_key,
        [schemas.MatchOut.model_validate(m).model_dump() for m in matches]
    )

    return matches

def update_match(db: Session, match_id: int, match_in: schemas.MatchUpdate):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        return None

    for field, value in match_in.model_dump(exclude_unset=True).items():
        setattr(match, field, value)

    db.commit()
    db.refresh(match)

    delete_cache(f"match:{match_id}")
    delete_cache("matches:all")

    return match

def delete_match(db: Session, match_id: int):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        return None

    db.delete(match)
    db.commit()

    delete_cache(f"match:{match_id}")
    delete_cache("matches:all")

    return match
