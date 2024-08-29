
from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_management_system.settings')

app = Celery('project_management', broker="redis://redis:6379/0", backend="redis://redis:6379/0")
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kathmandu')

app.config_from_object(settings, namespace='CELERY')

#celery beat settings
app.autodiscover_tasks() 


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
