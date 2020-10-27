"""
Load/update references to FAC PDF and Excel files.
"""

import csv
import os
from datetime import datetime

from django.db import transaction

from distiller.data.models import ETLLog
from ...gateways import files
from .. import models


def _parse_date(date_str: str):
    return datetime.strptime(date_str, '%m/%d/%Y')


def _yield_documents_from_csv(reader):
    for row in reader:
        yield models.FacDocument(
            version=row['VERSION'],
            audit_year=row['AUDITYEAR'],
            dbkey=row['DBKEY'],
            file_type=row['file_type'],
            file_name=row['file_name'],
            # report_id=row['REPORTID'],
            # ein=row['EIN'],
            # fy_end_date=_parse_date(row['FYENDDATE']),
            # fac_accepted_date=_parse_date(row['FACACCEPTEDDATE']),
            # date_received=_parse_date(row['DATERECEIVED']),
        )


@transaction.atomic
def load_fac_csvs(
    # Load all files from this path prefix
    source_dir: str,
    # Clear the target table before loading
    reload: bool = False,
    # Number of rows to INSERT per batch
    batch_size: int = 1_000,
    log_to_db: bool = False,
):
    """
    Load all CSVs in `source_dir` to FacDocument.
    """

    if reload:
        models.FacDocument.objects.all().delete()

    csv_paths = files.glob(os.path.join(source_dir, '*'))
    for csv_path in csv_paths:
        with files.input_file(csv_path) as csv_file:
            models.FacDocument.objects.bulk_create(
                _yield_documents_from_csv(csv.DictReader(csv_file)),
                batch_size=batch_size
            )

    if log_to_db:
        ETLLog.objects.log_fac_document_crawl(source_dir)


def _yield_documents_from_filenames(file_paths):
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        # Format: 10165120181.pdf
        base, extension = file_name.split('.')
        file_type = 'form' if extension == 'xlsx' else 'audit'
        yield models.FacDocument(
            version=base[-1],
            audit_year=base[-5:-1],
            dbkey=base[:-5],
            file_type=file_type,
            file_name=file_name,
        )


@transaction.atomic
def load_fac_bucket(
    # Load all files from this path prefix
    source_dir: str,
    # Clear the target table before loading
    reload: bool = True,
    # Number of rows to INSERT per batch
    batch_size: int = 1_000,
    log_to_db: bool = False,
):
    """
    Load all documents that are in the document store (S3 in production)
    """

    if reload:
        models.FacDocument.objects.all().delete()

    files.glob(f'{source_dir}/**')

    crawled_files = files.glob(os.path.join(source_dir, '*'))
    models.FacDocument.objects.bulk_create(
        _yield_documents_from_filenames(crawled_files),
        batch_size=batch_size
    )

    if log_to_db:
        ETLLog.objects.log_fac_document_crawl(source_dir)
