# Task M1-004: Validate/init archive root structure

## Goal
When Archive Root is set, validate expected structure and initialize missing folders.

## Scope
- Define required top-level dirs (minimal for MVP):
  - people/
- When POST /config/archive-root is called:
  - create required dirs if missing
  - refuse if root is not writable
- Add “show archive root in config response”.

## Non-goals
- No media/photos/recordings dirs yet unless you want them in MVP structure.
- No manifests/hashing.

## Steps
1) Add backend helper validate_archive_root(path).
2) Ensure it creates required folders.
3) Add tests around creating missing folders.

## Acceptance checks
- Set archive root to an empty temp dir -> backend creates people/ automatically.
- Setting to read-only dir fails with helpful error.

## Definition of Done
- [x] Initialization is deterministic
- [x] Errors are actionable

## Status
- [x] Completed (2025-12-13)
