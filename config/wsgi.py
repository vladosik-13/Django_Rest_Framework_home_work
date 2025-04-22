import os
from django.core.wsgi import get_wsgi_application
from config.celery import app as celery_app


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")

application = get_wsgi_application()

celery_app.autodiscover_tasks()
