# Tasks system

- Each file in tasks/ is a unit of work.
- Work order is controlled by active_task.md (set via tools/set-task.sh).
- Each task includes: Goal, Scope/Non-goals, Steps, Acceptance checks, DoD.

Conventions:
- One task => one PR (recommended).
- If a bug is found, create a new task under tasks/REGRESSIONS/.
