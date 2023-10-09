#!/bin/bash

echo "Running makemigrations"
python manage.py makemigrations

echo "Running migrations"
python manage.py migrate

python manage.py spectacular --file schema.yml

exec "$@"