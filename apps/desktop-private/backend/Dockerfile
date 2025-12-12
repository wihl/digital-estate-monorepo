FROM python:3.11-slim

# Set working directory to the monorepo root initially to copy packages
WORKDIR /app

# Copy the shared package and install it
COPY packages/ingest-logic ./packages/ingest-logic
RUN pip install -e ./packages/ingest-logic

# Now setup the backend
WORKDIR /app/apps/desktop-private/backend

COPY apps/desktop-private/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY apps/desktop-private/backend .

# The WORKDIR is already set correctly for the backend to run
