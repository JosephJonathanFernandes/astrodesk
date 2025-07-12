#!/bin/bash
set -e

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download ephemeris data if it doesn't exist
echo "Checking for ephemeris data..."
python -c "
from skyfield.api import load
import os
print('Downloading ephemeris data...')
eph = load('de421.bsp')
print('Ephemeris data downloaded successfully!')
"

echo "Build process completed successfully!" 