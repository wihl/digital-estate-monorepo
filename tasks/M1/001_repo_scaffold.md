# Task M1-001: Repo scaffold (backend + frontend + dev commands)

## Goal
Create a runnable repo skeleton with FastAPI backend and Jinja2/HTMX frontend, plus standard dev commands.

## Scope
- Add backend scaffold (FastAPI) with /health.
- Add frontend scaffold with a placeholder page.
- Add Makefile (or just scripts) so later tasks can run predictable commands.

## Non-goals
- No archive logic yet.
- No DB yet.

## Steps
1) Create folders: backend/, frontend/, tools/, tasks/.
2) Backend: FastAPI app with GET /health returning { "ok": true }.
3) Frontend: minimal app that loads and shows "Digital Estate MVP".
4) Add dev commands:
   - backend: `make dev-backend` (or equivalent)
   - frontend: `make dev-frontend`
   - tests placeholder: `make test` (even if minimal)

## Acceptance checks
- `make dev-backend` starts server and `curl localhost:8000/health` returns ok.
- `make dev-frontend` starts UI and loads in browser.

## Definition of Done
- [ ] Repo runs backend + frontend locally
- [ ] README includes setup prerequisites (python 3.11+, node)
