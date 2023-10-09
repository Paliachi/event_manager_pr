# Run&Build docker container
build:
	docker-compose up --build

# Run Docker container
up:
	docker-compose up

# Run Makemigrations
makemigrations:
	docker-compose exec api python manage.py makemigrations

# Run Migrations:
migrate:
	docker-compose exec api python manage.py migrate

# Run Tests:
tests:
	docker-compose exec api python manage.py test
