# Show available commands
default:
    @just --list

# Setup Python project
init:
    uv sync
    fnm use
    cd mta-sign-ui && pnpm install

# Build frontend and run FastAPI serving static files
run: build-ui
    uv run python main.py

# Development mode: Next.js dev server + FastAPI backend (hot reload for both)
dev:
    #!/usr/bin/env bash
    set -e
    echo "Starting FastAPI backend on :8000..."
    uv run python main.py &
    BACKEND_PID=$!
    echo "Starting Next.js dev server on :3000..."
    cd mta-sign-ui && pnpm dev &
    FRONTEND_PID=$!
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
    echo ""
    echo "Development servers running:"
    echo "  Frontend: http://localhost:3000 (with hot reload)"
    echo "  Backend:  http://localhost:8000 (API only)"
    echo ""
    wait

# Run only the backend (for when you want to run frontend separately)
dev-backend:
    FRONTEND_ENABLE=false uv run python main.py

# Run only the frontend dev server
dev-frontend:
    cd mta-sign-ui && pnpm dev

# Lint Python project with ruff
lint:
    uv run ruff check .

# Auto fix Python lint with ruff
lint-fix:
    uv run ruff check . --fix

# Run backend tests
test-backend:
    uv run pytest tests/ -v

# Run frontend tests
test-frontend:
    cd mta-sign-ui && pnpm test

# Run all tests
test: test-backend test-frontend

# Build frontend for production
build-ui:
    cd mta-sign-ui && pnpm build
    rm -rf static
    cp -r mta-sign-ui/out static

# Build multi-arch container image
containers:
    podman build --platform linux/arm64,linux/amd64 -f docker/Dockerfile --manifest chaos2theory/pi-mta-sign:test .
    podman manifest push --all chaos2theory/pi-mta-sign:test
    podman manifest rm chaos2theory/pi-mta-sign:test

# Build container image (local arch only)
build-container:
    podman build -f docker/Dockerfile -t pi-mta-sign:local .
