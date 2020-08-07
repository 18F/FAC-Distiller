
"""
Use apscheduler to run a daily job to refresh the source tables.
"""

import random
import sys
import time

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import (
    DjangoJobStore, register_events, register_job
)

from .etls import load_dumps


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


@register_job(
    scheduler,
    'cron',
    hour=0,
    timezone=pytz.timezone('US/Eastern'),
    replace_existing=True
)
def download_and_update_tables():
    for table in load_dumps.FAC_TABLES_NAMES:
        sys.stdout.write(f'Downloading table "{table}"...\n')
        sys.stdout.flush()
        load_dumps.download_table(
            table,
            target_dir=settings.LOAD_TABLE_ROOT
        )
    for table in load_dumps.FAC_TABLES_NAMES:
        sys.stdout.write(f'Loading FAC table "{table}"...\n')
        sys.stdout.flush()
        load_dumps.update_table(
            table,
            source_dir=settings.LOAD_TABLE_ROOT,
        )


register_events(scheduler)
scheduler.start()
