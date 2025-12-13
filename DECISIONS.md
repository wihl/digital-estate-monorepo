# Architectural Decisions

## 001. Stack Selection (2025-12)
- **Backend**: FastAPI (Python 3.11+).
- **Frontend**: Server-side rendered **Jinja2** templates with **HTMX** for interactivity.
  - *Context*: We removed the React frontend to simplify the stack/build process and rely on Python ecosystem strength.
- **Dev Env**: Docker Compose.

## 002. Storage Engine
- **Filesystem**: ExFAT (External SSD) as the primary store.
- **Index**: SQLite with FTS5 for search capabilities.
  - *Reasoning*: SQLite is ubiquitous, simple, and capable enough for single-user desktop usage.

## 003. Configuration Location
- Application config (last opened archive path, theme, etc.) is stored in the User's Home Directory:
  - `~/Library/Application Support/DigitalEstateMVP/config.json` (Mac)
  - `~/.config/digital-estate-mvp/config.json` (Linux)
- This separates "App State" from "Archive Data".
