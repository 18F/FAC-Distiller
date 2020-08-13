"""
This module contains a Django management command to extract
findings, corrective action plans, and keywords from uploaded PDFs in
S3.
"""

from decimal import Decimal

from django.core.management.base import BaseCommand

from ...models import AssistanceListing


class Command(BaseCommand):
    help = "Prints active CFDA prefixes of the form XX.X"

    def handle(self, *args, **options):
        cfdas = AssistanceListing.objects.all().order_by(
            'program_number').values_list('program_number', flat=True)
        prefixes = set('%04.1f' % Decimal(cfda) for cfda in cfdas)
        for prefix in sorted(prefixes):
            print(prefix)
