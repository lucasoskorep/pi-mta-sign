# Run tests and linters
@default: run

# Setup project
@init:
  poetry install

# Setup project
@run:
  poetry run uvicorn server:app --reload --port 8000
