#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../../.." && pwd )"

# Add the project root and backend to PYTHONPATH
export PYTHONPATH=$PROJECT_ROOT/src/backend:$PYTHONPATH

# Activate virtual environment if it exists
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Check if test mode is requested
if [ "$1" == "--test" ]; then
    echo "Running model test..."
    cd "$PROJECT_ROOT"
    python -m synthetic_data.test_model
else
    # Run the application
    cd "$PROJECT_ROOT"
    python src/backend/synthetic_data/main.py
fi 