# Task M1-007: Create person (person.yaml + timeline.yaml) using ruamel.yaml

## Goal
Implement POST /people to create a new Person folder with person.yaml and timeline.yaml.

## Scope
- POST /people accepts minimal fields:
  - given, surname, birth_date (optional), etc.
- Writes YAML using ruamel.yaml round-trip so future edits preserve comments/order.
- Use safe_write for all writes.
- Create timeline.yaml with schema_version and empty timeline list.

## Non-goals
- No edit endpoints yet.

## Steps
1) Add minimal YAML schemas for person.yaml and timeline.yaml.
2) Write files to sharded person folder.
3) Return created person id and path.

## Acceptance checks
- POST /people creates directory and files.
- YAML includes schema_version: 1 and required keys.

## Definition of Done
- [ ] Uses safe_write
- [ ] Uses ruamel.yaml
