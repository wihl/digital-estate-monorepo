# Task M1-001: Repo scaffold (backend + frontend + dev commands)

## Goal
Create a runnable repo skeleton with FastAPI backend which serves Jinja2/HTMX, plus standard dev commands.

## Scope
- Add backend scaffold (FastAPI) with /health.
- Add Makefile (or just scripts) so later tasks can run predictable commands.

## Non-goals
- No archive logic yet.
- No DB yet.

## Steps
1) Create folders: backend/, tools/, tasks/.
2) Backend: FastAPI app with GET /health returning {"status": "ok", "message": "Backend is running"}.
3) Add dev commands:
   - backend: `make dev-backend` (or equivalent)
   - tests placeholder: `make test` (even if minimal)

## Acceptance checks
- `make dev-backend` starts server and `curl localhost:8000/health` returns ok.


## Definition of Done
- [ ] Repo runs backend locally
- [ ] README includes setup prerequisites (python 3.11+, node)

## Status
Completed: 2025-12-13
Commit: [main ec52ceb]
Notes: (optional)


