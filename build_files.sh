#!/bin/bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python packages from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Run Django collectstatic command
python manage.py collectstatic

# Add console.log statements to debug the issue
console.log("Python version: " + process.version)
console.log("PATH: " + process.env.PATH)
