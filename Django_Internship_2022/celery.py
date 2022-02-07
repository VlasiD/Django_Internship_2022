import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Internship_2022.settings')

celery_app = Celery('Django_Internship_2022')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()