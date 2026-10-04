#!/usr/bin/env bash

set -e

if ! command -v python >/dev/null 2>&1; then
    echo "Python is not installed."
    echo "Installing Python through uv..."
fi

if ! command -v uv >/dev/null 2>&1; then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    export PATH="$HOME/.local/bin:$PATH"
fi

uv python install 3.14 --default
uv sync

python db_setup.py

echo "Setup completed successfully."