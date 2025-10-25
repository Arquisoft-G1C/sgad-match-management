# main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import engine, Base, get_db
import requests
import redis
from dotenv import load_dotenv
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Create tables if not exist (for prototype)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Match Management Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configs from env
REFEREE_SERVICE_URL = os.getenv("REFEREE_SERVICE_URL", "http://localhost:8001")  # adjust
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis client (simple sync client for prototype)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def publish_event(channel: str, payload: dict):
    try:
        redis_client.publish(channel, str(payload))
    except Exception as e:
        # don't break main flow if redis is down; log in production
        print("Redis publish failed:", e)

def referee_exists_and_available(referee_id: int) -> bool:
    """
    Simple validation: call Referee Management: GET /referees/{id}
    Expect 200 with availability flag optionally.
    """
    try:
        url = f"{REFEREE_SERVICE_URL}/referees/{referee_id}"
        resp = requests.get(url, timeout=3)
        if resp.status_code != 200:
            return False
        data = resp.json()
        # Expect data like {"id":..., "available": true}
        if isinstance(data, dict):
            return data.get("available", True)  # default True if not provided
        return True
    except requests.RequestException:
        # If referee service unreachable, return False to avoid bad assignment.
        return False

@app.post("/matches", response_model=schemas.MatchOut, status_code=status.HTTP_201_CREATED)
def create_match(match_in: schemas.MatchCreate, db: Session = Depends(get_db)):
    # Validate referee with Referee Management
    if not referee_exists_and_available(match_in.referee_id):
        raise HTTPException(status_code=400, detail="Referee not found or not available")

    db_match = crud.create_match(db, match_in)
    # Publish event to Redis
    publish_event("match_events", {"type": "match_created", "match_id": db_match.id})
    return db_match

@app.get("/matches", response_model=List[schemas.MatchOut])
def list_matches(skip: int = 0, limit: int = 100, referee_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.list_matches(db, skip=skip, limit=limit, referee_id=referee_id)

@app.get("/matches/{match_id}", response_model=schemas.MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    obj = crud.get_match(db, match_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Match not found")
    return obj

@app.put("/matches/{match_id}", response_model=schemas.MatchOut)
def update_match(match_id: int, match_in: schemas.MatchUpdate, db: Session = Depends(get_db)):
    # If referee_id is updated, validate it
    if match_in.referee_id is not None:
        if not referee_exists_and_available(match_in.referee_id):
            raise HTTPException(status_code=400, detail="Referee not found or not available")

    updated = crud.update_match(db, match_id, match_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Match not found")
    publish_event("match_events", {"type": "match_updated", "match_id": match_id})
    return updated

@app.delete("/matches/{match_id}", response_model=schemas.MatchOut)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_match(db, match_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Match not found")
    publish_event("match_events", {"type": "match_deleted", "match_id": match_id})
    return deleted
  
