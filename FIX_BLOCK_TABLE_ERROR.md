# Fixing the "relation 'block' does not exist" Error on Render.com

This guide provides step-by-step instructions to fix the database table initialization error you're experiencing on Render.com.

## The Problem

Based on the error logs, your application is connecting to the PostgreSQL database correctly, but the database tables haven't been created. This is causing the error:

```
psycopg2.errors.UndefinedTable: relation "block" does not exist
```

## Solution 1: Run Database Migrations Manually

1. **Access the Render Shell**:
   - Go to your web service on Render.com
   - Click on the "Shell" tab

2. **Run the Database Initialization Script**:
   ```bash
   python init_render_db.py
   ```

   This script will:
   - Check your database connection
   - Create all necessary tables using SQLAlchemy's `db.create_all()`
   - Create an admin user
   - Verify the tables were created correctly

3. **Restart Your Service**:
   - After running the initialization script, go back to the "Overview" tab
   - Click on "Manual Deploy" → "Deploy latest commit"

## Solution 2: Update the Start Command in render.yaml

Your current `render.yaml` file should be using the prestart.sh script, but it may not be working correctly. If the manual approach above works, let's fix the automatic deployment:

1. **Check the prestart.sh File Permissions**:
   ```bash
   chmod +x prestart.sh
   ```

2. **Create a Build Script**:
   Create a file named `build_render.sh` with the following content:
   ```bash
   #!/bin/bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Initialize database tables
   python init_render_db.py
   
   echo "Build completed successfully!"
   ```

3. **Update render.yaml**:
   Update your `render.yaml` to use the build script:
   ```yaml
   services:
     - type: web
       name: ittoken-web
       runtime: python
       region: frankfurt
       buildCommand: bash build_render.sh
       startCommand: gunicorn app.wsgi:app
       # ...other settings
   ```

4. **Push Changes** and redeploy

## Solution 3: Run Migrations Directly

If the above solutions don't work, try running the migrations directly:

```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

## Verifying the Fix

After applying any of these solutions:

1. **Check the Database Tables**:
   ```bash
   python check_database_tables.py
   ```

2. **Visit Your Application**: If the tables were created successfully, your application should now work without the "relation does not exist" error.

## Troubleshooting

If you're still experiencing issues:

1. **Check the Render Environment Variables**:
   Make sure `DATABASE_URL` is set correctly and points to the Render-provided PostgreSQL database.

2. **Check Database Permissions**:
   Make sure your database user has permissions to create tables.

3. **Review Logs**: Look at the application logs on Render for any errors during table creation.

4. **Connection Details**: Run the following to check connection details:
   ```bash
   python debug_render_db.py
   ```
