"""
This module contains a Django management command to load assistance listings
from beta.sam.gov into the database.

Assistance Listings include metadata about programs receiving grant funding.
"""

import sys

from django.core.management.base import BaseCommand

from ...etls import single_audit_db


class Command(BaseCommand):
    help = 'Load tables from the Single Audit Database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Load all supported FAC tables',
        )
        for table in single_audit_db.FAC_TABLES_NAMES:
            parser.add_argument(
                f'--{table}',
                action='store_true',
                help=f'Load {table} FAC table',
            )

    def handle(self, *args, **options):
        for table in single_audit_db.FAC_TABLES_NAMES:
            if options['all'] or options[table]:
                sys.stdout.write(f'Loading FAC table "{table}"...\n')
                sys.stdout.flush()
                single_audit_db.update_table(table)
