import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Internship_2022.settings')

celery_app = Celery('Django_Internship_2022')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
celery_app.conf.timezone = 'UTC'

CELERY_BEAT_SCHEDULER = {
    'update weather every day at 7:00': {
        'task': 'cities.tasks.add_weather',
        'schedule': crontab(hour=7, minute=0),
        },
    'delete weather entries older than 7 days': {
        'task': 'cities.tasks.delete_old_entries',
        'schedule': crontab(hour=7, minute=0),
    },
}