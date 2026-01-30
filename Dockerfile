# Stage 1: Build the Next.js frontend
FROM docker.io/library/node:25-alpine AS frontend-builder
LABEL authors="lucasoskorep"

WORKDIR /build/mta-sign-ui

# Enable corepack for pnpm
RUN corepack enable && corepack prepare pnpm@10.28.1 --activate

# Copy package files first for better caching
COPY mta-sign-ui/package.json mta-sign-ui/pnpm-lock.yaml* ./

# Install dependencies (use frozen-lockfile if lock exists, otherwise generate)
RUN pnpm install

# Copy the rest of the frontend source
COPY mta-sign-ui/ ./

# Build the static export (outputs to 'out' directory)
RUN pnpm build

# Stage 2: Python backend with frontend static files
FROM ghcr.io/astral-sh/uv:python3.13-bookworm
LABEL authors="lucasoskorep"

WORKDIR /app

# Copy dependency files and install dependencies only (not the project itself)
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy source code
COPY mta_api_client ./mta_api_client
COPY mta_sign_server ./mta_sign_server
COPY main.py stops.txt ./

# Copy the built frontend from the first stage
COPY --from=frontend-builder /build/mta-sign-ui/out ./static

# Now install the project
RUN uv sync --frozen --no-dev

EXPOSE 8000

ENTRYPOINT ["uv", "run", "python", "main.py"]
