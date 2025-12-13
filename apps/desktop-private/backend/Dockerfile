FROM python:3.11-slim

# Set working directory to the monorepo root initially to copy packages
WORKDIR /app

# Copy the shared package and install it
# Copy the shared package and install it
COPY packages/ingest-logic ./packages/ingest-logic
RUN --mount=type=cache,target=/root/.cache/pip pip install -e ./packages/ingest-logic

# Now setup the backend
WORKDIR /app/apps/desktop-private/backend

COPY apps/desktop-private/backend/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Copy backend code
COPY apps/desktop-private/backend .

# The WORKDIR is already set correctly for the backend to run
