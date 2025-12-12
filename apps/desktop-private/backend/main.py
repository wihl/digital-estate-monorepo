from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ingest_logic.common.fs_utils import write_safe
from ingest_logic.common.yaml_utils import load_yaml, save_yaml
import os
from routers import people

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(people.router)

@app.get("/health")
def read_root():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/api/config")
def read_config():
    return {"environment": "local-dev", "storage": "ExFAT", "mount": os.getenv("SSD_MOUNT_PATH")}

@app.post("/api/test-safe-write")
def test_safe_write():
    mount_path = os.getenv("SSD_MOUNT_PATH", "/data")
    test_file = os.path.join(mount_path, "test_safe.yaml")
    
    try:
        data = {"test": "safe_write", "status": "pending"}
        save_yaml(test_file, data)
        
        # Verify
        loaded = load_yaml(test_file)
        if loaded["test"] != "safe_write":
             raise Exception("Verification failed")
             
        return {"status": "success", "file": test_file, "content": loaded}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
