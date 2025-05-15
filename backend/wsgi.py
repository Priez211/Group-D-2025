import os
import sys

# Add your project directory to the sys.path
path = '/home/malual211/Group-D-2025/backend'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'aits.production'

# Create application object
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 