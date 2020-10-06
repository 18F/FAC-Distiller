"""
This module contains a Django management command to print CFDA prefixes for FAC
audits. This utility is intended to be used by the `/bin/crawl` script, so we
can target Scrapy crawls to prefixes that have actual audits in the database.
"""

import re
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db.models import Max

from ...models import Audit


class Command(BaseCommand):
    help = "Prints the date range of the unloaded processed date ranges."

    def handle(self, *args, **options):
        last_accepted_date = Audit.objects.aggregate(
            Max('fac_accepted_date')
        )['fac_accepted_date__max']
        print(
            last_accepted_date.strftime('%m/%d/%Y'),
            datetime.now().strftime('%m/%d/%Y'),
        )
