# crm/celery.py
import os
from celery import Celery

# set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

app = Celery("crm")

# load settings from Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# auto-discover tasks in all apps
app.autodiscover_tasks()
