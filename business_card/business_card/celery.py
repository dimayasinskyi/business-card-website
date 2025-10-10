import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_card.settings')

app = Celery('business_card')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()