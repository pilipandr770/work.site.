#!/bin/bash
# build_render.sh - Run during the build phase on Render.com

echo "=== STARTING BUILD PROCESS ==="

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make scripts executable
echo "Making scripts executable..."
chmod +x prestart.sh
chmod +x *.py

# Initialize database tables using robust method
echo "Initializing database tables using robust strategy..."
python robust_db_init.py

# Specifically fix the block table issue
echo "Fixing block table issue..."
python fix_block_table.py

# Verify database tables exist
echo "Final verification of database tables..."
python check_database_tables.py

echo "=== BUILD PROCESS COMPLETED ==="
