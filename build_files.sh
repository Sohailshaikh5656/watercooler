#!/bin/bash

echo "Python version: $(python --version)"
echo "PATH: $PATH"

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python packages from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Run Django collectstatic command
python manage.py collectstatic
