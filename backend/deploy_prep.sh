#!/bin/bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a superuser if needed (uncomment and modify as needed)
# python manage.py createsuperuser

echo "Deployment preparation completed!" 