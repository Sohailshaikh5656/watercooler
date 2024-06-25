#!/bin/bash

# Activate virtual environment using vercel python
vercel python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python packages from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Run Django collectstatic command
python manage.py collectstatic
