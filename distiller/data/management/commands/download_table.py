"""
This module contains a Django management command to download source table dumps
into a central location.
"""

import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from ...etls import single_audit_db


class Command(BaseCommand):
    help = 'Download table dump(s) from upstream source location'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Load all supported tables',
        )
        for table in single_audit_db.FAC_TABLES_NAMES:
            parser.add_argument(
                f'--{table}',
                action='store_true',
                help=f'Download {table} table',
            )

    def handle(self, *args, **options):
        for table in single_audit_db.FAC_TABLES_NAMES:
            if options['all'] or options[table]:
                sys.stdout.write(f'Downloading table "{table}"...\n')
                sys.stdout.flush()
                single_audit_db.download_table(
                    table,
                    target_dir=settings.DEFAULT_IMPORT_DIR
                )
