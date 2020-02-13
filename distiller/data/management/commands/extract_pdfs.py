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
        parser.add_argument("pdf_ids", nargs="*", type=int)

    def handle(self, *args, **options):
        nlp = extract_pdf.setup()
        pdf_ids = options["pdf_ids"]
        if options["all"]:
            pdf_ids = extract_pdf.get_all_pdfs()
            sys.stdout.write("Extracting all PDFs ...\n")
            sys.stdout.flush()

        for pdf_id in pdf_ids:
            sys.stdout.write(f'Extracting PDF id "{pdf_id}"...\n')
            sys.stdout.flush()
            extract_pdf.process_audit_pdf(nlp, pdf_id)
