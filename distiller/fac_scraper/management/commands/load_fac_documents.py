"""
This module contains a Django management command to download source table dumps
into a central location.
"""

import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from ...etls import fac_documents


class Command(BaseCommand):
    help = 'Load FAC documents to database from the scraper-produced CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--load-dir',
            help='Subdirectory of `FAC_CRAWL_ROOT` to load CSVs from',
        )
        parser.add_argument(
            '--reload',
            action='store_true',
            help='Clear table before loading',
        )

    def handle(self, *args, **options):
        sys.stdout.write(f'Loading files from "{options["load_dir"]}"...\n')
        sys.stdout.flush()
        fac_documents.load_fac_csvs(
            source_dir=os.path.join(settings.FAC_CRAWL_ROOT, options['load_dir']),
            reload=options['reload'],
        )
