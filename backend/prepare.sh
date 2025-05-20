#!/bin/bash
set -e

echo "Running migrations..."
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput 

echo "Preparation completed successfully!" 