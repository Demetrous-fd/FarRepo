from datetime import timedelta
import os

from celery import Celery

from app.settings import settings


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", settings.redis_dsn)
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", settings.redis_dsn)
celery.conf.redbeat_redis_url = os.environ.get("CELERY_REDBEAT", settings.redis_dsn)

celery.conf.update(
    timezone='Europe/Moscow', 
    enable_utc=True,
    worker_hijack_root_logger=False
)

celery.conf.beat_schedule = {
    'update_posts': {
        'task': 'app.tasks.farpost.update_farpost_data',
        'schedule': timedelta(seconds=settings.update_posts_interfal_in_seconds)
    }
}
