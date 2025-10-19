#!/bin/bash

# -------------------------------
# Dev script to run FastAPI app
# -------------------------------

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Make sure we are in project root
cd "$(dirname "$0")" || exit  # Change to script directory (project root)

echo "Starting FastAPI app in development mode..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
