#!/bin/bash
if [ ! -d "migrations" ]; then
    echo "Initializing migrations directory..."
    flask db init
    if [ $? -ne 0 ]; then
        echo "Error: Failed to initialize migrations. Check run.py and flask-migrate setup."
        exit 1
    fi
else
    echo "Migrations directory already exists."
fi