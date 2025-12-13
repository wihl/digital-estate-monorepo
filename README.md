# Digital Estate MVP

A minimal viable product for managing digital estate assets, focused on ingestion and person management.

## Tech Stack
- **Backend**: Python 3.11+, FastAPI
- **Frontend**: Server-side rendered Jinja2 templates with HTMX
- **Infrastructure**: Docker, Docker Compose
- **Storage**: Local filesystem (ExFAT optimized)

## Prerequisites
- **Python**: 3.11 or higher
- **Docker**: Desktop or Engine (required for full stack execution)
- **Make**: (Optional) for running dev scripts

## Getting Started

### Running with Docker (Recommended)
The easiest way to run the application is via Docker Compose:

```bash
# Build and start services
docker compose up --build
```

Access the application at: http://localhost:8000

### Local Development
To run the backend locally without Docker:

1.  **Navigate to backend**:
    ```bash
    cd apps/desktop-private/backend
    ```

2.  **Install dependencies**:
    ```bash
    # Create venv
    python3.11 -m venv venv
    source venv/bin/activate
    
    # Install backend deps
    pip install -r requirements.txt
    
    # Install shared logic (editable mode)
    pip install -e ../../../packages/ingest-logic
    ```

3.  **Run Server**:
    ```bash
    uvicorn main:app --reload
    ```

## Configuration
- **TRANSCRIPTION_PROVIDER**: Control transcription engine. Options: `local` (default) or `gemini`.
- **SSD_MOUNT_PATH**: Path to storage root. Defaults to `./tmp_data`.

## Project Structure
- `apps/desktop-private/backend`: FastAPI application and templates.
- `packages/ingest-logic`: Shared Python logic for identity, storage, and transcription.
- `tasks/`: Task definitions and backlog.
- `tmp_data/`: default local storage for uploads.
