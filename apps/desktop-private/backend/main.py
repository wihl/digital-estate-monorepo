from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ingest_logic.common.fs_utils import write_safe, write_safe_stream
from ingest_logic.common.yaml_utils import load_yaml, save_yaml
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

STORAGE_ROOT = os.getenv("SSD_MOUNT_PATH", "/data")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/import/recording")
async def import_recording(file: UploadFile = File(...)):
    if not file.filename:
         raise HTTPException(status_code=400, detail="No file filename")

    content_type = file.content_type or ""
    
    # Determine type
    if "video" in content_type:
        subdir = "video"
    elif "audio" in content_type:
        subdir = "audio"
    else:
        # Default to video if unknown, or maybe a 'misc' folder? 
        # Requirement says "recordings/audio or recordings/video". 
        # Let's fallback to video for now or reject? 
        # Let's be permissive and default to video if unsure but extension matters.
        subdir = "video"

    target_dir = os.path.join(STORAGE_ROOT, "recordings", subdir)
    os.makedirs(target_dir, exist_ok=True)
    
    target_path = os.path.join(target_dir, file.filename)
    
    try:
        # 1. Save File Securely
        await write_safe_stream(target_path, file)
        
        # 2. Generate sidecar
        meta_path = target_path + ".yaml"
        metadata = {
            "original_filename": file.filename,
            "content_type": content_type,
            "ingest_status": "pending_transcription",
             # Ideally usage of datetime.now() but user said "No Node.js" etc... so standard python is fine.
             # but remember user said local time source of truth is passed in prompt. 
             # We can't access that easily here in the running app. 
             # We'll just generate a basic skeleton.
        }
        save_yaml(meta_path, metadata)

        return {"status": "success", "filename": file.filename, "path": target_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/api/config")
def read_config():
    return {"environment": "local-dev", "storage": "ExFAT", "mount": STORAGE_ROOT}
