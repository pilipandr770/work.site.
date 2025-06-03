# Deploying IT Token to Render.com

This guide provides step-by-step instructions for deploying your IT Token application to render.com with PostgreSQL.

## Prerequisites

Before you begin, ensure you have:
- A render.com account
- Your code pushed to a Git repository (GitHub, GitLab, etc.)
- The latest code changes committed, including the render.yaml file

## Deployment Options

You have two options for deployment:

### Option 1: Manual Deployment (Recommended for First-Time Setup)

#### Step 1: Create a PostgreSQL Database

1. Log in to your render.com dashboard
2. Click "New" → "PostgreSQL"
3. Configure your database:
   - **Name**: `ittoken-db` (or your preferred name)
   - **Database**: `ittoken_db`
   - **User**: Leave as default
   - **Region**: Choose closest to your users
   - **Plan**: Select appropriate plan
4. Click "Create Database"
5. **Important**: Note down the connection details provided

#### Step 2: Create a Web Service

1. Click "New" → "Web Service"
2. Connect your GitHub/GitLab repository
3. Configure the service:
   - **Name**: `ittoken`
   - **Environment**: Python
   - **Region**: Same as your database
   - **Branch**: main (or your default branch)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
4. Click "Create Web Service"

#### Step 3: Configure Environment Variables

1. Go to your new web service
2. Click on "Environment" tab
3. Add the following environment variables:
   - `DATABASE_URL`: Copy the Internal Database URL from your PostgreSQL database info page
     - It should look like: `postgresql://user:password@host:port/database_name`
     - **IMPORTANT**: Do NOT use your local database URL with localhost or 127.0.0.1
   - `SECRET_KEY`: A secure random string
   - `TOKEN_CONTRACT_ADDRESS`: Your Ethereum contract address
   - `TOKEN_RECEIVER_ADDRESS`: Your Ethereum receiver address
   - `PYTHONUNBUFFERED`: `true`
4. Click "Save Changes"

#### Step 4: Run Database Migrations

1. Go to your web service's "Shell" tab
2. First verify your database connection:
   ```
   python render_db_check.py
   ```
3. If the connection is successful, run database migrations:
   ```
   python -m app.migrations_update
   ```
4. Verify tables were created:
   ```
   python check_render_postgres.py
   ```

### Option 2: Blueprint Deployment (Automated)

1. Make sure the `render.yaml` file is in your repository
2. Log in to your render.com dashboard
3. Click "New" → "Blueprint"
4. Select your repository
5. Review the resources that will be created
6. Click "Apply" to deploy automatically

## Verifying Deployment

After deployment completes:

1. Click on your web service's "Logs" tab to check for any errors
2. Run the database check script:
   ```
   python check_render_postgres.py
   ```
3. Visit your application URL to confirm it's working correctly

## Troubleshooting

### Database Connection Issues

If you see errors like "connection refused" or "could not connect to server":

1. Verify your DATABASE_URL is correctly set in environment variables
   - Go to your PostgreSQL database in Render
   - Find the "Connections" section
   - Copy the "Internal Database URL" 
   - Paste this URL as your DATABASE_URL environment variable
2. Make sure it's not trying to connect to localhost
   - The URL should contain your Render-hosted database address, not localhost or 127.0.0.1
3. Check that the PostgreSQL service is running
4. Verify network connectivity between your services
   - Your web service and database must be in the same region

### Migration Issues

If tables are not being created:

1. Run migrations manually:
   ```
   python -m app.migrations_update
   ```
2. Check migration logs for errors
3. Verify database permissions

## Key Points About the Database Connection

### Your `app/config.py` is Correctly Set Up

Your application is already correctly configured to use environment variables:

```python
# Database configuration with PostgreSQL support
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Fix for Heroku PostgreSQL URL
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
else:
    # Fallback to SQLite for development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
```

### What You Need to Do on Render.com

1. **Never use localhost/127.0.0.1 in Render's environment variables**
2. **Always use the Internal Database URL provided by Render**
3. **Set the DATABASE_URL environment variable in your web service**

For detailed instructions with screenshots, see the `RENDER_DATABASE_ENV_GUIDE.md` file.

## Next Steps

1. Set up automatic deploys from your Git repository
2. Configure custom domains for your application
3. Set up monitoring and alerts
4. Consider adding a CDN for static assets

For additional help, consult the render.com documentation at https://render.com/docs
