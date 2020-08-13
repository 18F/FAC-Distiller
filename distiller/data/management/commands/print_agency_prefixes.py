"""
This module contains a Django management command to extract
findings, corrective action plans, and keywords from uploaded PDFs in
S3.
"""

import re
from decimal import Decimal

from django.core.management.base import BaseCommand

from ...models import CFDA


class Command(BaseCommand):
    help = "Prints active CFDA prefixes of the form XX.X"

    def handle(self, *args, **options):
        # Use a regex to match the parts, because the FAC has some CFDAs
        # with letters - eg, "84.U42" and "97.IPA"
        cfda_regex = re.compile('(\d\d)\.(.*)')
        prefixes = set()

        cfdas = CFDA.objects.all().values_list('cfda', flat=True)
        for cfda in cfdas:
            match = cfda_regex.match(cfda)
            prefix = f'{match.group(1)}.{match.group(2)[0]}'
            prefixes.add(prefix)

        for prefix in sorted(prefixes):
            print(prefix)
