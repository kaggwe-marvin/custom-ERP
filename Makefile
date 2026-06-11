.PHONY: run lint format test migrate

run dev:
	poetry run daphne config.asgi:application

# 	poetry run python manage.py runserver

migrations:
	poetry run python manage.py makemigrations apps_iam
	poetry run python manage.py makemigrations core_finance
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


pipeline: clear migrations migrate format lint test
