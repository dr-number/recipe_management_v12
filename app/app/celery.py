import os

from celery import Celery
from celery.schedules import crontab

from app.settings import DEBUG

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

app.conf.beat_schedule = {
    'clear_finam_catalog_tools': {
        'task': 'clear_finam_catalog_tools',
        'schedule': crontab(hour=7, minute=50, day_of_week='6'),
    },
    'task_add_log_portfolio': {
        'task': 'task_add_log_portfolio',
        'schedule': crontab(hour=0, minute=0, day_of_week='1-5'),
    },
}
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.conf.update(
    worker_hijack_root_logger=False,
)

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()