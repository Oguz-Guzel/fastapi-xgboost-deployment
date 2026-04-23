# 1. Use a lightweight Python base image
FROM python:3.11-slim

# 2. Install uv directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy the lockfile and project settings first
# This is an optimization: if your code changes but your dependencies don't, 
# Docker will skip the expensive 'uv sync' step.
COPY pyproject.toml uv.lock ./

# 5. Install dependencies into the container
RUN uv sync --frozen --no-cache

# 6. Copy the rest of the application (app, src, models)
COPY . .

# 7. Expose the port FastAPI runs on
EXPOSE 8000

# 8. Start the server
# We use 'uv run' so it uses the virtual environment uv created inside the container
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]