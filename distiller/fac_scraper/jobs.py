"""
Use apscheduler to run a daily job to refresh the source tables.
"""

import os
import subprocess

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import (
    DjangoJobStore, register_events, register_job
)


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


@register_job(
    scheduler,
    'cron',
    hour=1,
    timezone=pytz.timezone('US/Eastern'),
    replace_existing=True
)
def daily_document_crawl():
    crawl_path = os.path.join(settings.BIN_DIR, 'crawl')
    subprocess.run([crawl_path])


register_events(scheduler)
scheduler.start()
