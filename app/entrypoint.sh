#!/bin/bash

echo "🔐 Carregando variáveis de ambiente do SSM Parameter Store..."

aws ssm get-parameter \
  --name "/cobraii/.env.prod" \
  --with-decryption \
  --query Parameter.Value \
  --output text > .env

echo "✅ .env carregado. Exportando variáveis..."
export $(cat .env | xargs)

echo "📦 Rodando make migrations..."
python manage.py makemigrations  --noinput

echo "📦 Rodando migrações..."
python manage.py migrate --noinput

echo "📁 Coletando estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Subindo o Gunicorn..."
exec gunicorn project.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --worker-class sync \
  --timeout 300
