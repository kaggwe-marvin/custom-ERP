.PHONY: run lint format test migrate

run dev:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate

format:
	poetry run black .

lint:
	poetry run mypy .

test:
	poetry run pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} \;
	find . -type f -name "*.pyc" -delete


start pipeline: format lint test
