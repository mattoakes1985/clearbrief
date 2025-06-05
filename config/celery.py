# config/celery.py

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('clearbrief')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks([
    'apps.news',
])


app.conf.beat_schedule = {
    'fetch-sources-every-30-minutes': {
        'task': 'apps.news.tasks.fetch_sources.fetch_sources_task',
        'schedule': crontab(minute='*/30'),
    },
}
