#!/bin/bash
set -e

# If DB host & port are provided separately, wait for DB
if [[ -n "$DB_HOST" && -n "$DB_PORT" ]]; then
  echo "Waiting for database $DB_HOST:$DB_PORT..."
  until nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 1
  done
  echo "Database is ready!"
else
  echo "Skipping DB wait (DB_HOST or DB_PORT not set)"
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn chowfast_backend.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind "0.0.0.0:${PORT:-8000}"
