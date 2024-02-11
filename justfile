# Run tests and linters
@default: run

# Setup project
@init:
  poetry install

# Setup project
@run:
  poetry run python main.py


# Lint project with ruff linter
@lint:
  poetry run ruff .

# Auto fix lint with ruff
@lint-fix:
  poetry run ruff . --fix

@containers:
  podman build -f python.dockerfile -t pi-mta-sign:latest . --load