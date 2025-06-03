# Render.com Deployment Checklist

## Pre-Deployment

1. [x] Verify `render.yaml` configuration
2. [x] Ensure `requirements.txt` is up to date
3. [x] Set up database initialization scripts
4. [x] Configure environment variables

## Deployment Process

1. [ ] Deploy to Render.com
   - Connect GitHub repository
   - Select branch to deploy
   - Verify build settings
   - Start deployment

2. [ ] Monitor build process
   - Check for successful dependency installation
   - Verify database initialization completes
   - Watch for any errors in the build logs

3. [ ] Check application health
   - Verify app is running
   - Check database connection
   - Test admin login

## Troubleshooting

If deployment fails, run the following checks:

1. [ ] Check build logs for errors
2. [ ] Verify environment variables in Render dashboard
3. [ ] Connect to Render shell and run:

```bash
# Check database connection
python debug_render_db.py

# Verify database tables
python check_database_tables.py

# Run robust initialization if needed
python robust_db_init.py

# If all else fails, try direct SQL initialization
python direct_sql_init.py
```

## Post-Deployment

1. [ ] Create initial content (blocks, products, etc.)
2. [ ] Test all features
3. [ ] Set up monitoring

## Important Notes

- If you make changes to database models, commit the changes and redeploy
- The application uses PostgreSQL on Render.com, not SQLite
- Admin credentials: username=`admin`, password=`admin` (change after first login)
