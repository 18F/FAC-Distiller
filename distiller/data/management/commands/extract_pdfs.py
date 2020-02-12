"""
This module contains a Django management command to extract
findings, corrective action plans, and keywords from uploaded PDFs in
S3.
"""

import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from ...etls import extract_pdf


class Command(BaseCommand):
    help = "Extract PDF text from audits where applicable"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all", action="store_true", help="Extract all PDFs",
        )
        parser.add_argument("audit_ids", nargs="*", type=int)

    def handle(self, *args, **options):
        nlp = extract_pdf.audit_pdf_setup()
        audit_ids = options["audit_ids"]
        if options["all"]:
            audit_ids = extract_pdf.get_all_audits_with_pdf()
            sys.stdout.write("Extracting all PDFs from relevant audits ...\n")
            sys.stdout.flush()

        for audit_id in audit_ids:
            sys.stdout.write(f'Extracting PDF from audit "{audit_id}"...\n')
            sys.stdout.flush()
            extract_pdf.process_audit_pdf(nlp, audit_id)
