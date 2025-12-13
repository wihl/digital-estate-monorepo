#!/usr/bin/env bash
set -euo pipefail
task_path="${1:-}"
if [[ -z "$task_path" ]]; then
  echo "Usage: $0 tasks/M1/001_repo_scaffold.md"
  exit 1
fi
if [[ ! -f "$task_path" ]]; then
  echo "No such task: $task_path"
  exit 1
fi

cat > active_task.md <<EOF
Current task: $task_path
Rules:
- Follow INVARIANTS.md (filesystem source of truth; SQLite is disposable index; ruamel.yaml round-trip).
- Implement only what is in the current task.
- Keep changes small and focused; avoid refactors.
- Stop when Definition of Done is satisfied.
EOF

echo "Active task set to $task_path"
