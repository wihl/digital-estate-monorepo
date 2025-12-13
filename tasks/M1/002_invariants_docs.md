# Task M1-002: Add INVARIANTS.md + DECISIONS.md + PITFALLS.md

## Goal
Create minimal “tribal knowledge” docs to constrain future AI work.

## Scope
- Add INVARIANTS.md with bullet non-negotiables.
- Add DECISIONS.md with initial entries (stack, data ownership rules).
- Add PITFALLS.md stub.

## Non-goals
- Don’t over-document; keep each file < 2 pages.

## Steps
1) Create INVARIANTS.md with:
   - filesystem is source of truth
   - SQLite is disposable cache/index (FTS5)
   - ruamel.yaml round-trip preserves comments/order
   - safe-write required for all file writes
   - ExFAT constraints: no symlinks, case-insensitive filenames
2) Create DECISIONS.md with initial decisions:
   - FastAPI + React
   - SQLite FTS5
   - Config location (home app support dir)
3) Create PITFALLS.md stub with format “symptom/cause/fix”.

## Acceptance checks
- N/A (docs)

## Definition of Done
- [ ] Files exist and are concise
