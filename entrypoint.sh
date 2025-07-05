#!/bin/sh

echo "Waiting for database..."

# Resolve DB_HOST_NAME to its IPv4 address
# This is crucial for environments where IPv6 connectivity might be an issue (like Docker)
# It finds the first IPv4 address for the hostname.
DB_IPV4_HOST=$(getent hosts "$DB_HOST_NAME" | awk '{print $1}' | grep -E '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$' | head -n 1)

if [ -z "$DB_IPV4_HOST" ]; then
  echo "Error: Could not resolve IPv4 address for $DB_HOST_NAME. Exiting."
  exit 1
fi

echo "Resolved $DB_HOST_NAME to IPv4: $DB_IPV4_HOST"

until PGPASSWORD="$DB_PASSWORD" psql -h "$DB_IPV4_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is ready"

echo "Applying database migrations..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

echo "Starting Django server..."
exec "$@"