# Ensuring Your Application Uses PostgreSQL on Render.com

This guide will help you set up your IT Token application to use PostgreSQL on render.com.

## Setup Steps

1. **Create a New PostgreSQL Database on Render.com**
   - Go to your Render dashboard
   - Click on "New" and select "PostgreSQL"
   - Give it a name (e.g., "ittoken-db")
   - Choose an appropriate plan and region
   - Create the database and note the connection details

2. **Update Environment Variables in Your Web Service**
   - Go to your web service on Render
   - Navigate to the "Environment" tab
   - Add or update the following variable:
     ```
     DATABASE_URL=<your-postgresql-connection-string>
     ```
   - Make sure your other environment variables are also set:
     ```
     SECRET_KEY=<your-secret-key>
     TOKEN_CONTRACT_ADDRESS=0xAf6087a1A730DAb2CA8d42dca7893c22fDBA683d
     TOKEN_RECEIVER_ADDRESS=0x917544120060Feb4571CdB14dBCC1e4d8005c218
     ```

3. **Alternative: Use render.yaml for Infrastructure as Code**
   - Use the provided `render.yaml` file to set up both the web service and database
   - Run these commands to deploy using the render.yaml:
     ```
     render blueprint create
     ```

## Post-Deployment Steps

1. **Initialize the Database**
   - After the service is deployed, go to your service's shell
   - Run the following command to create the tables:
     ```
     python -m app.migrations_update
     ```

2. **Verify Database Connection**
   - Check your application logs to verify that the PostgreSQL connection is established
   - You should see a message indicating successful connection to the database

## Troubleshooting

If you encounter any issues:

1. **Check Environment Variables**
   - Verify that DATABASE_URL is properly set on render.com
   - The format should be: `postgresql://username:password@hostname:port/database_name`

2. **Check Database Access**
   - Ensure that your render.com service has network access to the PostgreSQL database
   - Check if your IP is allowed in the database firewall settings

3. **Review Logs**
   - Check your application logs for database connection errors
   - Look for any SQLAlchemy error messages

For additional help, please refer to the [Render.com PostgreSQL documentation](https://render.com/docs/databases) or the [Flask-SQLAlchemy documentation](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/).
