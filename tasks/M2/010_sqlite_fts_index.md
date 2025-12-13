# Task M2-010: SQLite FTS5 index creation + index persons/timeline

## Goal
Create disposable SQLite FTS5 index and populate from filesystem.

## Scope
- SQLite db stored in user home app support dir (not on archive).
- FTS table indexes:
  - person name fields
  - person free text (if any)
  - timeline entry title/description
- Add POST /reindex endpoint.

## Non-goals
- No recordings yet.
- No photo metadata yet.

## Steps
1) Create sqlite module and migrations (create tables if not exist).
2) Implement rebuild: clear + rescan people + insert rows.
3) Expose POST /reindex.

## Acceptance checks
- POST /reindex returns counts.
- Searching for a name returns matching person.

## Definition of Done
- [ ] Index is rebuildable from scratch
