The AITS project is an academic issue tracking system built with Django for the backend and React for the frontend. It is designed to manage and track academic issues raised by students, handled by lecturers, and reviewed by academic registrars. The backend uses the Django REST Framework to provide APIs for authentication, issue management, and notifications, while the frontend uses React with Vite for fast development and a responsive user interface.

The system includes role-based access control, meaning different users (students, lecturers, registrars, and admins) see different dashboards and functionalities. Students can submit academic issues, lecturers can respond to those issues, and registrars have administrative controls such as managing users and viewing notifications.

The goal of the project is to streamline the issue resolution process within academic institutions, improve accountability, and enhance communication among stakeholders.

# Group-D-2025 Project

## Deployment Instructions for PythonAnywhere

### Prerequisites
- PythonAnywhere account
- Git repository access
- Domain name (if using custom domain)

### Deployment Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/Group-D-2025.git
   cd Group-D-2025
   ```

2. **Set Up Virtual Environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure PythonAnywhere Web App**
   - Go to Web tab in PythonAnywhere dashboard
   - Create a new web app
   - Choose Manual Configuration
   - Select Python version (3.8 or higher)
   - Set the following:
     - Source code: /home/yourusername/Group-D-2025
     - Working directory: /home/yourusername/Group-D-2025/backend
     - WSGI configuration file: /var/www/yourusername_pythonanywhere_com_wsgi.py

4. **Update WSGI Configuration**
   - Edit the WSGI configuration file
   - Replace the default content with the contents of `pythonanywhere_wsgi.py`
   - Update the paths to match your PythonAnywhere username

5. **Set Up Static Files**
   ```bash
   python manage.py collectstatic
   ```
   - Configure static files in PythonAnywhere:
     - URL: /static/
     - Directory: /home/yourusername/Group-D-2025/backend/static

6. **Database Setup**
   - For free tier: SQLite is already configured
   - For paid tier: Update DATABASES in production.py to use PostgreSQL

7. **Environment Variables**
   Set these in PythonAnywhere's Web app configuration:
   - SECRET_KEY
   - JWT_SECRET_KEY
   - Any other sensitive configuration

8. **Final Steps**
   - Run migrations: `python manage.py migrate`
   - Create superuser: `python manage.py createsuperuser`
   - Reload the web app in PythonAnywhere dashboard

### Troubleshooting
- Check error logs in PythonAnywhere dashboard
- Verify all paths in WSGI configuration
- Ensure static files are properly collected
- Check CORS settings if frontend can't connect

### Security Notes
- Keep your SECRET_KEY secure
- Regularly update dependencies
- Monitor error logs
- Use HTTPS (enabled by default in production settings)
