import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'smart_todo' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_todo.settings')

# Get the WSGI application for serving the Django project
application = get_wsgi_application()
