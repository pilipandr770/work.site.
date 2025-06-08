#!/bin/bash
# This script runs during the build phase on Render.com

# Install dependencies
pip install -r requirements.txt

# Apply database migrations to PostgreSQL
echo "Running database migrations..."
python -m app.migrations_update

# Create admin user if needed
# Uncomment this only if you need to create an admin user on first deployment
# echo "Creating admin user..."
# python create_admin.py

echo "Build script completed successfully!"
