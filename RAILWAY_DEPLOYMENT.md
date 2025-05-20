# Railway Deployment Guide

## Required Services

To deploy this application on Railway, you need:

1. **Main app service** (this repository)
2. **PostgreSQL database** (must be added as a separate service)

## Step 1: Add a PostgreSQL Database

Before deploying the main application:

1. Log in to your Railway dashboard
2. Click "New Project" or open your existing project
3. Click "Add Service" → "Database" → "PostgreSQL"
4. Wait for the database to provision

## Step 2: Deploy the Application

Once the database is provisioned:

1. Click "Add Service" → "GitHub Repo"
2. Select this repository
3. Configure environment variables if needed (most are set in the .env file and Dockerfile)
4. Deploy

## Step 3: Link Services

Ensure your app and database are connected:

1. Go to your application service
2. Click "Variables" in the top menu
3. Click "Add from service"
4. Select your PostgreSQL database
5. This will automatically add the DATABASE_URL variable

## Troubleshooting

### Database Connection Issues

If you see database connection errors:

1. Verify the DATABASE_URL variable is set in your application service
2. Check if the PostgreSQL service is running
3. You may need to manually create a database user with appropriate permissions

### Migration Errors

If migrations are failing:

1. You can manually run migrations via Railway CLI: `railway run python backend/manage.py migrate`
2. Check database logs for specific errors

## Environment Variables

The following variables are required:

- `DATABASE_URL` (automatically set when linking to PostgreSQL service)
- `SECRET_KEY` (set in .env file)
- `DEBUG` (defaults to False for production)
- `ALLOWED_HOSTS` (defaults include *.up.railway.app)

## Step 4: Deploy the Backend
1. Click on "New Project"
2. Select "Deploy from GitHub repo"
3. Connect to your GitHub account if not already connected
4. Select your repository
5. Set the root directory to `backend`
6. Add the following environment variables:
   - `SECRET_KEY` - A secure random string
   - `DEBUG` - Set to 'False'
   - `ALLOWED_HOSTS` - This should include `*.up.railway.app` (this is already set in settings.py)

## Step 5: Deploy and Run Migrations
1. The backend service will automatically use the DATABASE_URL environment variable
2. The deployment will automatically run migrations and collect static files through prepare.sh
3. If you need to manually run commands:
   - Go to your backend service dashboard's "Commands" tab
   - Run: `python manage.py migrate`
   - Run: `python manage.py collectstatic --noinput`

## Step 6: Deploy the Frontend
1. In your project dashboard, click "New"
2. Select "Deploy from GitHub repo"
3. Select the same repository
4. Set the root directory to `frontend`
5. Add the following environment variables:
   - `VITE_API_URL` - The URL of your backend (e.g., `https://your-backend.up.railway.app/api`)
6. Set the build command to: `npm install && npm run build`
7. Set the start command to: `npm run start`

## Step 7: Connect Frontend and Backend
1. Go back to your backend service
2. Add additional environment variables:
   - `CORS_ORIGIN_WHITELIST` - Add your frontend URL, e.g., `https://your-frontend.up.railway.app`
   - `CSRF_TRUSTED_ORIGINS` - Add your frontend URL, e.g., `https://your-frontend.up.railway.app`

## Step 8: Configure Custom Domain (Optional)
1. Select your frontend service
2. Go to "Settings"
3. Under "Domains", click "Generate Domain" or "Custom Domain"
4. Follow the instructions to set up your domain

## Step 9: Test the Deployment
1. Visit your frontend domain
2. Test login, registration, and other functionality
3. Check the logs in Railway dashboard if you encounter any issues

## Troubleshooting
If you encounter issues:
1. Check the logs in Railway dashboard
2. Make sure all environment variables are correctly set
3. Verify that migrations ran successfully
4. Ensure that the frontend is correctly configured to call the backend API
5. You may need to run the prepare.sh script manually if migrations don't run automatically 