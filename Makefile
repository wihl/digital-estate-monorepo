.PHONY: help dev up down logs shell clean test

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

review: ## have codex review the code
	codex -q "/review"

test: ## Run tests (Placeholder)
	@echo "Running tests..."
	docker compose exec backend pytest || echo "No tests infrastructure set up yet, skipping."

tests: test ## Alias for test

clean: ## Cleanup temporary files and artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
