import os
import sys

# Add your project directory to the sys.path
path = '/home/malual211/Group-D-2025/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aits.production')

# Activate your virtual environment
activate_this = '/home/malual211/.virtualenvs/myenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 