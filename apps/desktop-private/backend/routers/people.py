from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from ingest_logic.people.manager import PersonManager

router = APIRouter(prefix="/api/people", tags=["people"])

def get_manager():
    # In a real app, use dependency injection. For MVP, instantiate per request or use a global.
    mount_path = os.getenv("SSD_MOUNT_PATH", "/data")
    return PersonManager(mount_path)

class PersonCreate(BaseModel):
    name: str
    bio: str = ""

@router.get("/")
def list_people():
    return get_manager().list_people()

@router.post("/")
def create_person(person: PersonCreate):
    try:
        return get_manager().create_person(person.name, person.bio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{slug}")
def get_person(slug: str):
    p = get_manager().get_person(slug)
    if not p:
        raise HTTPException(status_code=404, detail="Person not found")
    return p
