#!/bin/sh

# Wait for PostgreSQL to become available.
echo "Waiting for PostgreSQL to start..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start the Django app
echo "Starting Django..."
exec "$@"
