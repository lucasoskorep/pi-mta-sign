# Run tests and linters
@default: run

# Setup project
@init:
  poetry install

# Setup project
@run:
  poetry run uvicorn main:app --reload
