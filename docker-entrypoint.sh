#!/bin/sh
set -e

# Run database migrations if AUTO_MIGRATE is enabled
if [ "$AUTO_MIGRATE" = "true" ]; then
    echo "Running database migrations with Alembic..."
    alembic upgrade head
    echo "Database migrations completed."
fi

# Execute the main container command
exec "$@"
