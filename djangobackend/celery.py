
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangobackend.settings')

app = Celery('djangobackend')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc=False
app.autodiscover_tasks()
app.conf.update(timezone='Asia/Kolkata')

app.conf.broker_connection_retry_on_startup = True




# app.conf.beat_schedule = {
#             'print': {
#                 'task': 'home.tasks.printthis',
#                 'schedule':crontab(hour=14,minute=17) ,
#                 'args': (),
#             },
#         }
@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request|r}')