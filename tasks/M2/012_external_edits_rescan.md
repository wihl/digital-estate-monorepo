# Task M2-012: Detect external edits via mtime/size scan

## Goal
Ensure index doesn’t go stale if YAML is edited outside the app.

## Scope
- On backend startup (and/or on /reindex-lite endpoint):
  - scan person.yaml/timeline.yaml mtimes/sizes
  - if changed vs stored state table, reindex that person
- Simplify: maintain a table of file_path -> last_mtime,last_size.

## Non-goals
- No full filesystem watcher required.

## Steps
1) Add file_state table.
2) Implement fast scan and selective reindex.

## Acceptance checks
- Edit a YAML by hand; restart backend; search reflects change.

## Definition of Done
- [ ] Stale-index bug is prevented by design
