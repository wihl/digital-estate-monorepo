# Start from Python
FROM python:3.11-slim

# 1. Set the working directory to the 'root' of the container's monorepo
WORKDIR /monorepo

# 2. COPY the shared packages first (so they are available for pip)
COPY packages ./packages

# 3. COPY the backend requirements to their correct nested location
COPY apps/desktop-private/backend/requirements.txt ./apps/desktop-private/backend/requirements.txt

# 4. Change directory to where requirements.txt is
# This ensures the relative path "../../../packages" resolves correctly
WORKDIR /monorepo/apps/desktop-private/backend

# 5. Install dependencies
# Now pip can find "packages/contracts" by going up 3 levels
RUN pip install -r requirements.txt

# 6. Finally, copy the rest of the application code
COPY apps/desktop-private/backend .

# ... rest of your Dockerfile (CMD, EXPOSE, etc)