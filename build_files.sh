#!/bin/bash

# Install Python packages from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Run Django collectstatic command
python3.9 manage.py collectstatic
