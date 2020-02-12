import sys
import smart_open
import io
from datetime import datetime

from django.conf import settings

from . import nlp
from . import pdf_utils
from .analyze import analyze_doc
from ...gateways import files
from ..models.single_audit_db import Audit
from ..models.pdf_extract import PDFExtract


def audit_pdf_setup():
    return nlp.setup()


def get_all_audits_with_pdf():
    # for testing purposes
    # if True:
    #     Audit.objects.filter(id=64618).update(s3_url="data-sources/pdfs/14770920191.pdf")
    #     PDFExtract.objects.all().delete()
    # return Audit.objects.exclude(s3_url=None).values_list('pk', flat=True)
    return Audit.objects.all()[0].pk


def process_audit_pdf(processor, audit_id):
    try:
        audit = Audit.objects.get(id=audit_id)
        pdf = files.input_file(f"{settings.LOAD_TABLE_ROOT}/{audit.s3_url}", mode='rb')
        errors = pdf_utils.errors(pdf)
        if errors:
            sys.stdout.write(f'Could not read file: {errors}. Bailing out.\n')
            sys.stdout.flush()
            return

        page_length = pdf_utils.page_length(pdf)
        for page_number in range(0, page_length):
            sys.stdout.write(f'Processing {page_number}.\n')
            sys.stdout.flush()
            page_text = pdf_utils.page(pdf, page_number)
            page_doc = processor(page_text)
            results = analyze_doc(page_number, page_doc)
            for result in results:
                audit_num = result["audit"]
                sys.stdout.write(f'Found audit {audit_num} on page {page_number}.\n')
                sys.stdout.flush()
                PDFExtract(audit_year=audit.audit_year,
                           dbkey=audit.dbkey,
                           finding_ref_nums=audit_num,
                           finding_text=result["finding_text"],
                           cap_text=result["cap_text"],
                           last_updated=datetime.now(),
                ).save()

    except files.FileOpenFailure as e:
        sys.stdout.write(f'Could not read PDF: {e}, skipping...\n')
        sys.stdout.flush()
