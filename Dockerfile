FROM docker.io/library/node:25 AS frontend-builder
LABEL authors="lucasoskorep"

WORKDIR /build/mta-sign-ui

COPY mta-sign-ui/package.json mta-sign-ui/pnpm-lock.yaml* ./

RUN npm install -g pnpm

COPY mta-sign-ui/ ./

RUN pnpm install
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
