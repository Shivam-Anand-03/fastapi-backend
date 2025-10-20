#!/bin/bash
set -e  

if [ ! -d "migrations" ]; then
    echo "Initializing Alembic migrations..."
    alembic init -t async migrations
else
    echo "Migrations directory already exists, skipping init."
fi

echo "Running Alembic migration..."
alembic upgrade head

echo "Migration completed successfully!"
