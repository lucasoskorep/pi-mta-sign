FROM python:3.11-alpine

RUN pip install poetry

WORKDIR /app
COPY ../pyproject.toml poetry.lock ./

RUN poetry install --without dev

COPY ../mta_api_client ./
COPY ../mta_sign_server ./

COPY ../main.py stops.txt ./

ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]