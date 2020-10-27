"""
This module contains a Django management command to print CFDA prefixes for FAC
audits. This utility is intended to be used by the `/bin/crawl` script, so we
can target Scrapy crawls to prefixes that have actual audits in the database.
"""

import re
from decimal import Decimal

from django.core.management.base import BaseCommand

from ...models import CFDA


class Command(BaseCommand):
    help = "Prints active CFDA prefixes of the form XX.XX"

    def handle(self, *args, **options):
        # Use a regex to match the parts, because the FAC has some CFDAs
        # with letters - eg, "84.U42" and "97.IPA"
        cfda_regex = re.compile('(\d\d)\.([^\s]*)')
        prefixes = set()

        cfdas = CFDA.objects.all().values_list('cfda', flat=True)
        for cfda in cfdas:
            match = cfda_regex.match(cfda)

            # There are a few CFDAs that don't match the pattern, but
            # instead are just two-digit integers. Ignore these.
            if not match or not match.group(1) or not match.group(2):
                continue

            left = match.group(1).strip().upper()
            right = match.group(2).strip().upper()
            if not left or not right:
                continue

            prefix = f'{left}.{right[:2]}'
            prefixes.add(prefix)

        for prefix in sorted(prefixes):
            if not prefix.startswith('0'):
                print(prefix)
