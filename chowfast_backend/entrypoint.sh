#!/bin/bash
set -e

# Extract host and port from DATABASE_URL
DB_HOST=$(echo $DATABASE_URL | sed -E 's|.*/@([^:/]+).*|\1|')
DB_PORT=$(echo $DATABASE_URL | sed -E 's|.*:([0-9]+)/.*|\1|' || echo 5432)

echo "Waiting for $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do sleep 1; done
echo "DB ready!"

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

exec gunicorn chowfast_backend.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT:-8000}