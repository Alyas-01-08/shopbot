import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopWebBot.settings')
celery_app = Celery('shopWebBot')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
# celery_app.conf.beat_schedule = {
#     'set_profit_all_user_day': {
#         'task': 'bank.tasks.profit_all_user_day',
#         'schedule': crontab(minute=0, hour=23)}}
celery_app.conf.timezone = 'Europe/Moscow'
