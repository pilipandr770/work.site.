# Deploying to Render.com - Environment Variables Guide

This guide will help you correctly set up environment variables for your IT Token application on render.com.

## Required Environment Variables

When deploying to render.com, you need to set the following environment variables:

### Critical Variables

| Variable Name | Description | Example |
|---------------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string from render.com | `postgresql://user:password@host:port/database` |
| `SECRET_KEY` | Secret key for Flask sessions | `your-secure-secret-key` |
| `TOKEN_CONTRACT_ADDRESS` | Ethereum contract address | `0xAf6087a1A730DAb2CA8d42dca7893c22fDBA683d` |
| `TOKEN_RECEIVER_ADDRESS` | Ethereum receiver address | `0x917544120060Feb4571CdB14dBCC1e4d8005c218` |

### Optional Variables

| Variable Name | Description | Default |
|---------------|-------------|---------|
| `PYTHONUNBUFFERED` | Unbuffered Python output | `true` |
| `LANGUAGES` | Supported languages | `uk,en,ru` |

## Setting Up Environment Variables on Render.com

1. **Go to your Web Service** - Navigate to your web service in the render.com dashboard
2. **Navigate to Environment** - Click on the "Environment" tab
3. **Add Variables** - Add each of the required variables listed above
4. **Get PostgreSQL Connection String**:
   - Create a PostgreSQL database in render.com
   - Copy the connection string from the database details page
   - Set as `DATABASE_URL` environment variable

## Important: Do NOT Use Local Database URL

The error in your application is due to using a local PostgreSQL URL:

```
postgresql://postgres:Dnepr75ok613770@localhost:5433/ittoken_db
```

This won't work in production because:
1. There is no PostgreSQL server at localhost:5433 on render.com
2. The username, password, and database name are specific to your local setup

## Using Blueprint Deployment

If you prefer, you can use the provided `render.yaml` file for automatic setup:

1. **Add render.yaml** - Make sure the render.yaml file is in your GitHub repository
2. **Create Blueprint** - Use "New" → "Blueprint" in render.com dashboard
3. **Select Repository** - Connect to your GitHub repository
4. **Deploy** - Follow deployment instructions

The blueprint will automatically:
- Create a PostgreSQL database
- Set up your web service
- Configure environment variables
- Connect your web service to the database

## Checking Environment Variables

After deployment, verify your environment variables by:
1. Going to your service in render.com
2. Navigating to the "Environment" tab
3. Confirming all required variables are present and have correct values
