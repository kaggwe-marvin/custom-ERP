.PHONY: run dev migrate format lint test clear clean pipeline

run dev:
	poetry run daphne config.asgi:application

# poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate

format:
	poetry run black .

lint:
	poetry run mypy .

test:
	poetry run pytest

clear:
	clear

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} \;
	find . -type f -name "*.pyc" -delete

pipeline: migrate format lint test