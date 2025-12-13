# Task M1-008: Read/update person.yaml and timeline.yaml

## Goal
Implement GET/PUT endpoints for person.yaml and timeline.yaml.

## Scope
- GET /people/{id}/person.yaml -> returns raw YAML text + parsed summary (optional)
- PUT /people/{id}/person.yaml -> accepts YAML text, validates schema_version, safe writes
- Same for timeline.yaml
- Update “updated_at” in SQLite later (don’t do now)

## Non-goals
- No fancy UI editor.

## Steps
1) Implement file locate-by-id (scan index or deterministic path; simplest acceptable).
2) Validate YAML parses and has schema_version: 1.
3) Write via safe_write.

## Acceptance checks
- PUT then GET returns same YAML.
- Invalid YAML returns 400 with parse error.

## Definition of Done
- [ ] Safe_write used
- [ ] ruamel used for parse/round-trip where appropriate
