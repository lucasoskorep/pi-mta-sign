FROM docker.io/library/node:25 AS frontend-builder
LABEL authors="lucasoskorep"

WORKDIR /build/mta-sign-ui

COPY mta-sign-ui/package.json mta-sign-ui/pnpm-lock.yaml* ./

# Pin pnpm to the version declared in mta-sign-ui/package.json ("packageManager");
# an unpinned global install drifts to new majors (pnpm 12 hard-errors on
# unapproved build scripts).
RUN npm install -g pnpm@10.33.0

COPY mta-sign-ui/ ./

RUN pnpm install --frozen-lockfile
RUN pnpm build

FROM ghcr.io/astral-sh/uv:python3.13-bookworm
LABEL authors="lucasoskorep"

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY mta_api_client ./mta_api_client
COPY mta_sign_server ./mta_sign_server
COPY main.py stops.txt ./

COPY --from=frontend-builder /build/mta-sign-ui/out ./static

RUN uv sync --frozen --no-dev

EXPOSE 8000

ENTRYPOINT ["uv", "run", "python", "main.py"]
