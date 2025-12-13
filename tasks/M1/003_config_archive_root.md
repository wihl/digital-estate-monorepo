# Task M1-003: Local config + Archive Root selection endpoints

## Goal
Persist and retrieve Archive Root path via backend endpoints.

## Scope
- GET /config -> returns configured archive_root or null
- POST /config/archive-root -> sets archive_root (validates path exists)

## Non-goals
- No archive initialization yet (next task).
- No UI settings page yet.

## Steps
1) Implement config storage under ~/Library/Application Support/DigitalEstateMVP/config.json (or similar).
2) Add Pydantic models for request/response.
3) Add backend endpoints.

## Acceptance checks
- `curl localhost:8000/config` returns {"archive_root": null} initially.
- POST sets a valid existing path and GET returns it.

## Definition of Done
- [ ] Config persists across backend restarts
- [ ] Clear error on invalid path
