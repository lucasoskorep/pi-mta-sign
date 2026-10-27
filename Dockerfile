FROM ghcr.io/jdx/mise:2026.10.19-debian AS frontend-builder
LABEL authors="lucasoskorep"

WORKDIR /build/mta-sign-ui

COPY mise.toml ./
RUN mise trust && mise install node pnpm

COPY mta-sign-ui/package.json mta-sign-ui/pnpm-lock.yaml* ./

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
