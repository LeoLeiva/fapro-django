import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'faprodjango.config.settings.local')

app = Celery('uf', broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:global_settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-value-last-day': {
        'task': 'uf.tasks.update_last_day_value',
        'schedule': crontab(minute=0, hour=4)
    },
}
