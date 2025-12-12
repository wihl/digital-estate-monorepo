# Trigger reload (fix display_name)
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ingest_logic.common.fs_utils import write_safe, write_safe_stream
from ingest_logic.common.yaml_utils import load_yaml, save_yaml
from ingest_logic.people.manager import PersonManager
import os
import shutil
from routers import people
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(people.router)

templates = Jinja2Templates(directory="templates")

# Default to ./tmp_data for local dev if env var not set
# This matches the docker-compose volume mapping: ./tmp_data:/data
STORAGE_ROOT = os.getenv("SSD_MOUNT_PATH", os.path.abspath("./tmp_data"))
person_manager = PersonManager(STORAGE_ROOT)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    people_list = person_manager.list_people()
    return templates.TemplateResponse("index.html", {"request": request, "people": people_list})

@app.post("/api/people", response_class=HTMLResponse)
async def create_person(
    family_name: str = Form(...),
    given_name: str = Form(...),
    dob: str = Form(...),
    bio: str = Form("")
):
    try:
        person = person_manager.create_person(
            family=family_name,
            given=given_name,
            dob=dob,
            bio=bio
        )
        # Return an option tag to be appended to the select list
        return f'<option value="{person["slug"]}" selected>{person["display_name"]} ({person["id"]})</option>'
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/import/recording")
async def import_recording(
    file: UploadFile = File(...),
    person_slug: str = Form(...)
):
    if not file.filename:
         raise HTTPException(status_code=400, detail="No file filename")

    # Validate person
    person_data = person_manager.get_person(person_slug)
    if not person_data:
        raise HTTPException(status_code=404, detail="Person not found")

    content_type = file.content_type or ""
    
    # Determine type
    if "video" in content_type:
        subdir = "video"
    elif "audio" in content_type:
        subdir = "audio"
    else:
        # Fallback based on extension if content-type is missing/generic?
        # For now default to video as per prev logic, but let's be smarter if possible.
        # Simple for now.
        subdir = "video"

    # Directory Structure: people/{slug}/recordings/{audio|video}
    # Note: person_slug is relative path from people root, e.g. "shard/Name--ID"
    
    # We need to construct the full path manually since Manager doesn't manage recordings yet explicitly
    # But we know the structure.
    person_dir = os.path.join(STORAGE_ROOT, "people", person_slug)
    target_dir = os.path.join(person_dir, "recordings", subdir)
    
    os.makedirs(target_dir, exist_ok=True)
    
    target_path = os.path.join(target_dir, file.filename)
    
    try:
        # 1. Save File Securely
        await write_safe_stream(target_path, file)
        
        # 2. Generate sidecar
        # Fix: Remove extension from filename for yaml sidecar
        # e.g. interview.mp4 -> interview.yaml (not interview.mp4.yaml)
        file_stem = Path(file.filename).stem
        meta_path = os.path.join(target_dir, f"{file_stem}.yaml")
        
        metadata = {
            "original_filename": file.filename,
            "content_type": content_type,
            "ingest_status": "pending_transcription",
        }
        save_yaml(meta_path, metadata)

        return {"status": "success", "filename": file.filename, "path": target_path}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/api/config")
def read_config():
    return {"environment": "local-dev", "storage": "ExFAT", "mount": STORAGE_ROOT}
