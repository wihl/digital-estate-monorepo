# Task M1-005: Safe-write + tmp cleanup utilities

## Goal
Implement safe file writes appropriate for ExFAT and add startup cleanup of orphan temp files.

## Scope
- safe_write_text(path, content)
  - write to temp file in same dir
  - fsync
  - rename/replace target
- startup cleanup:
  - scan archive root for leftover *.tmp (define pattern)
  - delete or quarantine (choose simplest: delete)

## Non-goals
- No hashing/manifests.

## Steps
1) Create backend module filesystem/safe_write.py.
2) Use it nowhere yet (next tasks will integrate).
3) Add a simple unit test with temp dir.

## Acceptance checks
- Unit test verifies file content is correct after safe_write.
- If a fake *.tmp exists, startup cleanup removes it.

## Definition of Done
- [ ] Utility functions exist and are tested
- [ ] Cleanup runs at app startup (after archive root is configured)
