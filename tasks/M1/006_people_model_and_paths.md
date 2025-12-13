# Task M1-006: Person IDs, folder naming, scan people tree

## Goal
Implement person id generation and scanning people/**/person.yaml.

## Scope
- Define person id generator (base36) per your rules (simplify for MVP if needed).
- Person directory convention: "<Surname>, <Given>--<id>"
- Create sharded path under people/<2>/<2>/<dir>
- Implement GET /people scanning that returns basic list.

## Non-goals
- No UI yet.
- No editing yet.

## Steps
1) Implement id generation helper + normalization helpers (ExFAT-safe).
2) Implement scan that finds person.yaml under people/**.
3) Return a list: id, display name, path.

## Acceptance checks
- With fixture archive containing 2 people, GET /people returns both.

## Definition of Done
- [ ] Deterministic id + naming rules written down in DECISIONS.md
