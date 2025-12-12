FROM python:3.11-slim

WORKDIR /app/apps/desktop-private/backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We mount the volume at runtime, but copy here for build stability if needed
COPY . .

# Adjust workdir to run uvicorn
WORKDIR /app/apps/desktop-private/backend

# CMD is handled by docker-compose
