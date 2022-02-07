from .celery import celery_app

__all__ = ('celery_app',)
celery = celery_app