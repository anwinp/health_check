from celery import Celery
import os
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'report_generator.settings')

app = Celery('report_generator')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Set the broker URL to RabbitMQ
app.conf.broker_url = settings.CELERY_BROKER_URL

app.autodiscover_tasks()
