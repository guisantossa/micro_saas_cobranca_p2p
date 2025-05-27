#!/bin/sh

echo "✅ Aplicando migrations..."
poetry run python manage.py migrate

echo "✅ Coletando arquivos estáticos..."
poetry run python manage.py collectstatic --noinput

echo "✅ Iniciando servidor Django..."
poetry run python manage.py runserver 0.0.0.0:8000

celery -A project worker --loglevel=info
