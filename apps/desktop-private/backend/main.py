from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from ingest_logic.common.fs_utils import write_safe, write_safe_stream
from ingest_logic.common.yaml_utils import load_yaml, save_yaml
from ingest_logic.people.manager import PersonManager
from ingest_logic.transcription import TranscriptionManager
from ingest_logic.config import ConfigManager
from pydantic import BaseModel
import os
import shutil
from routers import people
from pathlib import Path
from ingest_logic.archive import bootstrap_archive, cleanup_temp_files
from contracts.models import Person

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

STORAGE_ROOT = os.getenv("SSD_MOUNT_PATH", os.path.abspath("./tmp_data"))
person_manager = PersonManager(STORAGE_ROOT)

transcription_manager = TranscriptionManager()
config_manager = ConfigManager()

# Background Task
def process_transcription(file_path: str, meta_path: str):
    try:
        print(f"Starting transcription for {file_path}...")
        transcript = transcription_manager.transcribe(file_path)
        
        # Save transcript
        txt_path = Path(file_path).with_suffix('.txt')
        with open(txt_path, 'w') as f:
            f.write(transcript)
            
        # Update metadata
        if os.path.exists(meta_path):
            meta = load_yaml(meta_path)
            meta['ingest_status'] = 'transcribed'
            # meta['transcript_path'] = str(txt_path) 
            save_yaml(meta_path, meta)
            
        print(f"Transcription complete: {txt_path}")
        
    except Exception as e:
        print(f"Transcription failed for {file_path}: {e}")
        # Update metadata to failed
        if os.path.exists(meta_path):
            meta = load_yaml(meta_path)
            meta['ingest_status'] = 'transcription_failed'
            meta['error_message'] = str(e)
            save_yaml(meta_path, meta)

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
        return f'<option value="{person.slug}" selected>{person.display_name} ({person.id})</option>'
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/import/recording")
async def import_recording(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    person_slug: str = Form(...),
):
    if not file.filename:
         raise HTTPException(status_code=400, detail="No file filename")

    # Validate person
    person_data = person_manager.get_person(person_slug)
    if not person_data:
        raise HTTPException(status_code=404, detail="Person not found")

    content_type = file.content_type or ""
    
    if "video" in content_type:
        subdir = "video"
    elif "audio" in content_type:
        subdir = "audio"
    else:
        subdir = "video"

    person_dir = os.path.join(STORAGE_ROOT, "people", person_slug)
    target_dir = os.path.join(person_dir, "recordings", subdir)
    
    os.makedirs(target_dir, exist_ok=True)
    
    target_path = os.path.join(target_dir, file.filename)
    
    try:
        await write_safe_stream(target_path, file)
        
        file_stem = Path(file.filename).stem
        meta_path = os.path.join(target_dir, f"{file_stem}.yaml")
        
        metadata = {
            "original_filename": file.filename,
            "content_type": content_type,
            "ingest_status": "pending_transcription",
        }
        save_yaml(meta_path, metadata)
        
        # Trigger background transcription
        background_tasks.add_task(process_transcription, target_path, meta_path)

        return {"status": "success", "filename": file.filename, "path": target_path, "message": "Upload complete. Transcription queued."}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/config")
def read_config():
    cfg = config_manager.load()
    return cfg

class ArchiveRootRequest(BaseModel):
    path: str

@app.post("/config/archive-root")
def set_archive_root(req: ArchiveRootRequest):
    # Normalize path once
    p = Path(req.path).expanduser().resolve()
    
    try:
        bootstrap_archive(p)
    except (ValueError, FileNotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=f"Permission denied: {e}")
    except OSError as e:
        print(f"Critical error initializing archive root: {e}") # Log to stdout/stderr
        raise HTTPException(status_code=500, detail="Failed to initialize archive root due to an internal system error.")
    
    config_manager.set_archive_root(str(p))
    # Cleanup any leftover temps in the new root
    cleanup_temp_files(p)
    return {"status": "updated", "archive_root": str(p)}

@app.on_event("startup")
async def startup_event():
    cfg = config_manager.load()
    if cfg.archive_root:
        p = Path(cfg.archive_root)
        if p.exists() and p.is_dir():
            count = cleanup_temp_files(p)
            if count > 0:
                print(f"Startup: Cleaned up {count} temporary files.")
