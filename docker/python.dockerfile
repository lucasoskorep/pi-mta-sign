FROM docker.io/library/python:3.11
LABEL authors="lucasoskorep"

WORKDIR /app

RUN apt-get update
RUN apt-get install -y \
    build-essential \
    curl

# Needed when building for obscure cpu architectures
#RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
#ENV PATH="/root/.cargo/bin:${PATH}"
#RUN cargo

RUN pip install poetry
COPY ../pyproject.toml poetry.lock ./
RUN poetry install --without dev
COPY ../mta_api_client ./
COPY ../mta_sign_server ./
COPY ../main.py stops.txt ./

ENTRYPOINT ["poetry", "run", "python", "-m", "main.py"]