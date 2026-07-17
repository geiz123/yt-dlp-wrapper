#!/bin/bash

VENV_HOME="./.venv"

# Change PYTHON_HOME if needed
# If python3 is already in your PATH, leave this as "python3"
# PYTHON_HOME="/usr/bin/python3"
# Or, for Homebrew:
# PYTHON_HOME="/opt/homebrew/bin/python3"
# Or, you install from python installer
PYTHON_HOME=/usr/local/bin/python3

VENV_ACTIVATION_SCRIPT="$VENV_HOME/bin/activate"

echo "************* Looking for Python at: $PYTHON_HOME"
echo "************* Expected VENV dir: $VENV_HOME"

echo "Starting..."
echo "Creating .venv..."

if "$PYTHON_HOME" -m venv .venv; then
    echo "Creating .venv...DONE"
else
    echo "*** ERROR creating virtual environment ***"
    exit 1
fi

echo "Activating virtual environment..."

# shellcheck source=/dev/null
source "$VENV_ACTIVATION_SCRIPT"

if [ $? -ne 0 ]; then
    echo "*** ERROR activating virtual environment ***"
    exit 1
fi

echo "Activating virtual environment...DONE"

echo "Installing requirements..."

if pip install -r requirements.txt; then
    echo "Installing requirements...DONE"
else
    echo "*** ERROR installing requirements ***"
    exit 1
fi

echo "Setup complete!"