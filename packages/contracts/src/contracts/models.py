from pydantic import BaseModel, Field, constr
from typing import List, Optional
from enum import Enum

# Strict validation patterns
BASE36_ID_PATTERN = r"^[a-zA-Z0-9_,.-]+$"

class PersonNameType(str, Enum):
    PRIMARY = "primary"
    ALIAS = "alias"
    MAIDEN = "maiden"

class PersonName(BaseModel):
    type: PersonNameType
    given: str = Field(min_length=1)
    surname: str = Field(min_length=1)
    suffix: str = Field(default="")

class PersonBirth(BaseModel):
    date: str = Field(..., description="ISO8601 Date String YYYY-MM-DD")

class PersonVitals(BaseModel):
    birth: PersonBirth

class Person(BaseModel):
    id: str = Field(..., pattern=BASE36_ID_PATTERN, description="Base36 ID from canonical Identity string")
    names: List[PersonName]
    vitals: PersonVitals
    bio: str = Field(default="")
    
    # Computed/Injected fields (Optional as they may not be present in raw storage)
    slug: Optional[str] = None
    display_name: Optional[str] = None

class IngestStatus(str, Enum):
    PENDING_TRANSCRIPTION = "pending_transcription"
    TRANSCRIBED = "transcribed"
    TRANSCRIPTION_FAILED = "transcription_failed"

class Recording(BaseModel):
    # ID is technically implicit (filename or file stem) in current legacy code,
    # but we should strictly define it if possible to match "Protobuf-style".
    # Using implicit ID from filename for now as per legacy behavior.
    
    original_filename: str = Field(min_length=1)
    content_type: str = Field(..., description="MIME type, e.g. video/mp4")
    ingest_status: IngestStatus
    
    # Optional fields
    error_message: Optional[str] = None
    transcript_path: Optional[str] = None
