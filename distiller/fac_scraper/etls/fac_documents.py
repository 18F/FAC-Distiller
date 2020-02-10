"""
Load/update references to FAC PDF and Excel files.
"""

import csv
import os
from datetime import datetime

from django.db import transaction

from ...gateways import files
from .. import models


def _parse_date(date_str: str):
    return datetime.strptime(date_str, '%m/%d/%Y')


def _yield_documents(reader):
    for row in reader:
        import pdb; pdb.set_trace()  #pylint: disable=C0321
        yield models.FacDocument(
            version=row['VERSION'],
            report_id=row['REPORTID'],
            audit_year=row['AUDITYEAR'],
            dbkey=row['DBKEY'],
            ein=row['EIN'],
            fy_end_date=_parse_date(row['FYENDDATE']),
            fac_accepted_date=_parse_date(row['FACACCEPTEDDATE']),
            date_received=_parse_date(row['DATERECEIVED']),
            file_type=row['file_type'],
            file_name=row['file_name'],
        )


@transaction.atomic
def load_fac_csvs(source_dir: str, batch_size: int = 1_000):
    """
    Load all CSVs in `source_dir` to FacDocument.
    """

    csv_paths = files.glob(os.path.join(source_dir, '*'))
    for csv_path in csv_paths:
        with files.input_file(csv_path) as csv_file:
            models.FacDocument.objects.bulk_create(
                _yield_documents(csv.DictReader(csv_file)),
                batch_size=batch_size
            )
