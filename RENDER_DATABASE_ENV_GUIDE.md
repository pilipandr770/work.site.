# Setting Up Database Environment Variables on Render.com

This guide provides step-by-step instructions with visual examples for setting up your PostgreSQL database connection on Render.com.

## Step 1: Create Your PostgreSQL Database

1. Go to your Render dashboard
2. Click "New" and select "PostgreSQL"

   ![New PostgreSQL](https://render.com/static/9c18f8877b8bc93b1763603d8a983a63/10d17/create-db.png)

3. Configure your database:
   - Name: `ittoken-db`
   - Database: `ittoken_db`
   - User: Leave as default
   - Region: Choose closest to your users
   - Plan: Select appropriate plan

4. Click "Create Database"

## Step 2: Get Your Database Connection URL

1. Once your database is created, go to the database dashboard
2. Find the "Connections" section
3. Copy the "Internal Database URL"

   ![Connection Info](https://docs.render.com/assets/images/database-connections-1c24513d1126b2fd7c85eaa1fd5effective.png)

   > **IMPORTANT**: Use the Internal Database URL for services running within Render.com

## Step 3: Set Environment Variables for Your Web Service

1. Go to your web service in the Render dashboard
2. Click on the "Environment" tab
3. Add a new environment variable:
   - Key: `DATABASE_URL`
   - Value: Paste the Internal Database URL you copied in Step 2

   ![Environment Variables](https://docs.render.com/assets/images/env-vars-3231ac95159ba5c9fb108cf0a783-3231ac95159ba5c9fb108cf0a783.webp)

4. Click "Save Changes"

## Step 4: Verify Your Connection

After setting your environment variables and deploying your service:

1. Go to your web service's "Shell" tab
2. Run the database check script:
   ```
   python render_db_check.py
   ```
   
   If successful, you should see:
   ```
   === RENDER DATABASE CONNECTION CHECKER ===

   ✅ Running on Render.com environment.
   ✅ DATABASE_URL environment variable is set and looks correct.
   URL Format: postgresql://****:****@dpg-example-host:5432/ittoken_db

   ✅ Your Render.com environment appears to be correctly configured for PostgreSQL!
   Your application should be able to connect to the database.

   === CHECK COMPLETE ===
   ```

## Common Issues and Solutions

### Issue: "Could not connect to server"
- **Solution**: Make sure you're using the Internal Database URL, not the External one

### Issue: "Password authentication failed"
- **Solution**: Double-check the URL provided by Render; don't modify the password

### Issue: Application tries to connect to localhost/127.0.0.1
- **Solution**: Make sure you've set the DATABASE_URL environment variable correctly on Render
- **Solution**: Check that your config.py is using the environment variable and not a hardcoded value

Remember: Your local development environment will still use your local database configuration, while the Render deployment will use the Render-provided PostgreSQL database.
