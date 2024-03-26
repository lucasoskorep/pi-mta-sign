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
  podman build --platform linux/arm64,linux/amd64 -f docker/python.dockerfile --manifest chaos2theory/pi-mta-sign:test .
  podman manifest push --all chaos2theory/pi-mta-sign:test
  podman manifest rm chaos2theory/pi-mta-sign:test