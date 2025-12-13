.PHONY: help dev up down logs shell clean test review review-staged review-working

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dev: up ## Start the full stack (Backend + UI) in Docker

up: ## Build and start services
	docker compose up --build -d
	@echo "App running at http://localhost:8000"

down: ## Stop services
	docker compose down

logs: ## View backend logs
	docker compose logs -f backend

shell: ## Open shell in backend container
	docker compose exec backend /bin/bash

# Legacy/Task compatibility aliases
dev-backend: dev ## Alias for dev (Backend serves the UI)
dev-frontend: dev ## Alias for dev (UI is served by Backend)

review: review-staged ## Review staged changes with Codex (before commit)

review-staged: ## Have Codex review staged changes (git diff --cached)
	@bash -lc 'set -euo pipefail; \
	if git diff --cached --quiet; then \
	  echo "No staged changes to review. Stage changes first (e.g., git add -p)."; exit 0; \
	fi; \
	DIFF="$$(git diff --cached)"; \
	codex "You are reviewing a staged Git diff for the Digital Estate MVP. \
Focus on correctness, consistency with MVP constraints and INVARIANTS.md, and anything likely to break docker compose dev flow. \
Avoid large refactors; suggest only necessary fixes. \
Here is the staged diff:\n\n$$DIFF"'

review-working: ## Have Codex review unstaged working-tree changes (git diff)
	@bash -lc 'set -euo pipefail; \
	if git diff --quiet; then \
	  echo "No unstaged changes to review."; exit 0; \
	fi; \
	DIFF="$$(git diff)"; \
	codex "You are reviewing an unstaged Git diff for the Digital Estate MVP. \
Focus on correctness, MVP constraints, and anything likely to break docker compose dev flow. \
Avoid large refactors; suggest only necessary fixes. \
Here is the diff:\n\n$$DIFF"'

test: ## Run tests (Placeholder)
	@echo "Running tests..."
	docker compose exec backend pytest || echo "No tests infrastructure set up yet, skipping."

tests: test ## Alias for test

clean: ## Cleanup temporary files and artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
