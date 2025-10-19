#!/bin/bash

# -------------------------------
# Dev script to run FastAPI app
# -------------------------------

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Navigate to the app folder
cd app || exit

# Run FastAPI using uvicorn in development mode
# --reload allows hot-reload on code changes
echo "Starting FastAPI app in development mode..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
