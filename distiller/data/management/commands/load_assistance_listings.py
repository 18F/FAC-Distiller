"""
This module contains a Django management command to load assistance listings
from beta.sam.gov into the database.

Assistance Listings include metadata about programs receiving grant funding.
"""

from django.core.management.base import BaseCommand

from ...etls import assistance_listings


class Command(BaseCommand):
    help = (
        'Refresh assistance listings table with most recent data.gov data, via'
        ' beta.sam.gov.'
    )

    def handle(self, *args, **options):
        assistance_listings.refresh()
