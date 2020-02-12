import sys
import smart_open
import io
from datetime import datetime

from django.conf import settings

from . import nlp
from . import pdf_utils
from .analyze import analyze
from ...gateways import files
from ..models.single_audit_db import Audit
from ..models.pdf_extract import PDFExtract
from ...fac_scraper.models import FacDocument


def setup():
    return nlp.setup()


def get_all_pdfs():
    # for testing purposes only
    if True:
        PDFExtract.objects.all().delete()
        FacDocument.objects.all().delete()
        # create a facsimile FacDocument to play with, linked to a random audit
        audit = Audit.objects.all()[0]
        FacDocument(
            version=1,
            report_id='1',
            audit_year=audit.audit_year,
            dbkey=audit.dbkey,
            ein='10',
            fy_end_date=datetime.now(),
            fac_accepted_date=datetime.now(),
            date_received=datetime.now(),
            file_type='audit',
            file_name='14770920191.pdf',
            audit=audit,
        ).save()
    return FacDocument.objects.all().values_list('pk', flat=True)


def process_audit_pdf(processor, pdf_id):
    try:
        document = FacDocument.objects.get(id=pdf_id)
        pdf = files.input_file(f"{settings.LOAD_TABLE_ROOT}/pdfs/{document.file_name}", mode='rb')
        errors = pdf_utils.errors(pdf)
        if errors:
            sys.stdout.write(f'Could not read file: {errors}. Bailing out.\n')
            sys.stdout.flush()
            return

        audit_results = analyze(processor, pdf)
        for result in audit_results:
            audit_num = result["audit"]
            sys.stdout.write(f'Found audit {audit_num}.\n')
            sys.stdout.flush()
            PDFExtract(audit_year=document.audit_year,
                       dbkey=document.dbkey,
                       finding_ref_nums=audit_num,
                       finding_text=result["finding_text"],
                       cap_text=result["cap_text"],
                       last_updated=datetime.now(),
            ).save()

    except files.FileOpenFailure as e:
        sys.stdout.write(f'Could not read PDF: {e}, skipping...\n')
        sys.stdout.flush()
