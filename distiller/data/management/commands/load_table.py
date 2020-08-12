"""
This module contains a Django management command to load assistance listings
from beta.sam.gov into the database.

Assistance Listings include metadata about programs receiving grant funding.
"""

import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from ...etls import load_dumps


class Command(BaseCommand):
    help = 'Load tables from the Single Audit Database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Load all supported FAC tables',
        )
        for table in load_dumps.FAC_TABLES_NAMES:
            parser.add_argument(
                f'--{table}',
                action='store_true',
                help=f'Load {table} FAC table',
            )
        parser.add_argument(
            '--log',
            action='store_true',
            help='Log to database',
        )

    def handle(self, *args, **options):
        for table in load_dumps.FAC_TABLES_NAMES:
            if options['all'] or options[table]:
                sys.stdout.write(f'Loading FAC table "{table}"...\n')
                sys.stdout.flush()
                load_dumps.update_table(
                    table,
                    source_dir=settings.LOAD_TABLE_ROOT,
                    log_to_db=options['log'],
                )
