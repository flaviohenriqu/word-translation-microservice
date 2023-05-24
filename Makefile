# Set the default target to `run`
.DEFAULT_GOAL := run

# Define variables
DOCKER_COMPOSE := docker-compose
DOCKER_RUN := $(DOCKER_COMPOSE) run --rm app
TEST_COMMAND := poetry run pytest tests/

# Build the Docker image
build:
	$(DOCKER_COMPOSE) build

# Start the application
run:
	$(DOCKER_COMPOSE) up

# Stop the application
stop:
	$(DOCKER_COMPOSE) down

# Run tests
test:
	$(DOCKER_RUN) $(TEST_COMMAND)

# Run tests with coverage
coverage:
	$(DOCKER_RUN) $(TEST_COMMAND) --cov=app --cov-report=html

# Format code using black
format:
	$(DOCKER_RUN) poetry run black app

# Lint code using flake8
lint:
	$(DOCKER_RUN) poetry run flake8 app

# Run type checking using mypy
typecheck:
	$(DOCKER_RUN) poetry run mypy app

# Clean up generated files and directories
clean:
	rm -rf .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete

# Generate and apply database migrations
migrate:
	$(DOCKER_RUN) poetry run alembic upgrade head

# Generate a new migration
migration:
	$(DOCKER_RUN) poetry run alembic revision --autogenerate -m "New migration"

# Show the current database revision
revision:
	$(DOCKER_RUN) poetry run alembic current

# Rollback the database to a previous revision
rollback:
	$(DOCKER_RUN) poetry run alembic downgrade -1

# Install Poetry dependencies
install:
	poetry install

.PHONY: build run stop test coverage format lint typecheck clean migrate migration revision rollback install
