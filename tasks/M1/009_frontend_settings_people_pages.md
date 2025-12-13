# Task M1-009: Frontend Settings + People list + Person detail

## Goal
Add minimal UI to drive archive root + person creation/editing.

## Scope
- Settings page:
  - shows current archive root
  - input to set archive root path
- People list:
  - list people from GET /people
  - button to create person
- Person detail:
  - view/edit person.yaml and timeline.yaml as raw textareas (MVP)

## Non-goals
- No polished UX.
- No routing perfection.

## Steps
1) Add basic routing (Settings / People / Person).
2) Wire to backend.
3) Add minimal error display.

## Acceptance checks
- Set root via UI, create person, edit YAML, refresh and see changes.

## Definition of Done
- [ ] Works end-to-end with fixture archive
