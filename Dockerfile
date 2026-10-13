# ==============================================================================
# Stage 1: Build & Dependency Installation
# ==============================================================================
FROM python:3.14-slim AS builder

# Install uv from official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation and copy link mode for caching
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies first (layer-cached)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --frozen --no-install-project --no-dev

# Copy application source code
COPY . /app

# Sync project package without dev dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# ==============================================================================
# Stage 2: Production Runtime
# ==============================================================================
FROM python:3.14-slim AS runner

# Install curl for container health checks and network diagnostics
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root system user
RUN groupadd -r appuser -g 10001 && \
    useradd -r -u 10001 -g appuser -d /home/appuser -m appuser

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application files with ownership
COPY --chown=appuser:appuser . /app

# Configure runtime environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    DEVICE=cpu \
    HF_HOME=/home/appuser/.cache/huggingface

# Ensure cache directory exists and permissions are set
RUN mkdir -p /home/appuser/.cache/huggingface && \
    chown -R appuser:appuser /home/appuser && \
    chmod +x /app/docker-entrypoint.sh

USER appuser

EXPOSE 8000

# Health check against /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["uvicorn", "main:server", "--host", "0.0.0.0", "--port", "8000"]
