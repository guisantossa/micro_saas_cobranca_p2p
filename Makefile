run:
	docker-compose up

build:
	docker-compose up --build

migrate:
	docker-compose run web poetry run python manage.py migrate

createsuperuser:
	docker-compose run web poetry run python manage.py createsuperuser

shell:
	docker-compose run web poetry run python manage.py shell

worker:
	docker-compose exec web poetry run celery -A project worker --loglevel=info

test:
	docker-compose run web poetry run python manage.py test

test-pytest:
	docker-compose run web poetry run pytest

make-migrations:
	docker-compose run web poetry run python manage.py makemigrations

test-coverage:
	docker-compose run web poetry run coverage run manage.py test
	docker-compose run web poetry run coverage report -m

lint:
	docker-compose run web poetry run flake8 core project users
