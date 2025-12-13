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

### Getting Started

We use `make` to manage the Docker-based development environment.

```bash
# Start the full stack (Backend + UI)
make dev

# View application logs
make logs

# Run tests
make test

# Open a shell inside the backend container
make shell

# Cleanup temporary files
make clean
```

Access the application at: http://localhost:8000

## Configuration
- **TRANSCRIPTION_PROVIDER**: Control transcription engine. Options: `local` (default) or `gemini`.
- **SSD_MOUNT_PATH**: Path to storage root. Defaults to `./tmp_data`.

## Project Structure
- `apps/desktop-private/backend`: FastAPI application and templates.
- `packages/ingest-logic`: Shared Python logic for identity, storage, and transcription.
- `tasks/`: Task definitions and backlog.
- `tmp_data/`: default local storage for uploads.
