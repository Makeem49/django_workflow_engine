from celery import Celery
import os
from django.conf import settings
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
