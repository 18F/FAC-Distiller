"""
This module contains a Django management command to load assistance listings
from beta.sam.gov into the database.

Assistance Listings include metadata about programs receiving grant funding.
"""

from django.core.management.base import BaseCommand

from ...etls import single_audit_db


class Command(BaseCommand):
    help = 'Load tables from the Single Audit Database'

    def handle(self, *args, **options):
        single_audit_db.update()
