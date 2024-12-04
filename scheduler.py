from celery import Celery
from celery.schedules import crontab

from celery_app import celery

celery.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'celery_app.fetch_data_and_create_plot',
        'schedule': 10.0,
    },
    'send-email-daily': {
        'task': 'celery_app.fetch_data_and_create_plot',
        'schedule': crontab(hour=0, minute=0),
    },
}
