# Task M2-011: /search endpoint (bounded scope)

## Goal
Expose GET /search?q=... and optional date filtering for timeline.

## Scope
- Query searches FTS and returns:
  - people matches
  - timeline matches
- Optional date range filtering for timeline entries when date exists.

## Non-goals
- No semantic/CV search.
- No photo/story unified search yet (later milestones).

## Steps
1) Implement query parsing.
2) Return ranked results with type field.

## Acceptance checks
- Search returns expected results against fixture archive.
- Empty query returns 400.

## Definition of Done
- [ ] Works quickly (<1s on fixture)
