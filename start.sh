#!/bin/bash
# This script runs when the application starts on Render.com

# Wait for PostgreSQL database to be ready
echo "Waiting for PostgreSQL database..."
sleep 5

# Verify database connection and run migrations if needed
echo "Verifying database setup..."
python -c "
import os
import time
import psycopg2
from urllib.parse import urlparse

# Parse DATABASE_URL to get connection parameters
url = urlparse(os.environ.get('DATABASE_URL'))
dbname = url.path[1:]  # Remove leading slash
user = url.username
password = url.password
host = url.hostname
port = url.port

# Try connecting until successful
max_attempts = 5
attempt = 0
while attempt < max_attempts:
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.close()
        print('Database connection successful!')
        break
    except Exception as e:
        attempt += 1
        print(f'Connection attempt {attempt} failed: {e}')
        if attempt < max_attempts:
            time.sleep(2)
        else:
            print('Could not connect to database after multiple attempts')
            import sys
            sys.exit(1)

# Run database migrations
print('Running migrations')
import subprocess
subprocess.run(['python', '-m', 'app.migrations_update'])
"

# Start the application
echo "Starting application..."
exec gunicorn run:app
