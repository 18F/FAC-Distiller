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
    help = 'Load FAC documents to database from a ListBucket operation on the S3 bucket'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reload',
            action='store_true',
            help='Clear table before loading',
        )
        parser.add_argument(
            '--log',
            action='store_true',
            help='Log to database',
        )

    def handle(self, *args, **options):
        sys.stdout.write(f'Loading files from "{settings.FAC_DOCUMENT_DIR}"...\n')
        sys.stdout.flush()
        fac_documents.load_fac_bucket(
            source_dir=settings.FAC_DOCUMENT_DIR,
            reload=options['reload'],
            log_to_db=options['log'],
        )
