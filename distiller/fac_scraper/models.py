from compositefk.fields import CompositeForeignKey
from django.db import models

from distiller.data.models import Audit


class FacDocument(models.Model):
    version = models.IntegerField()
    report_id = models.CharField(max_length=8)
    audit_year = models.DecimalField(
        max_digits=4,
        decimal_places=0,
        help_text='Audit Year and DBKEY (database key) combined make up the primary key.'
    )
    dbkey = models.CharField(
        max_length=6,
        help_text='Audit Year and DBKEY (database key) combined make up the primary key.'
    )
    ein = models.CharField(
        max_length=9,
        help_text='Employer Identification Number'
    )
    fy_end_date = models.DateField()
    fac_accepted_date = models.DateField()
    date_received = models.DateField()
    file_type = models.CharField(
        max_length=8,
        choices=(
            ('form', 'form'),
            ('audit', 'audit'),
        )
    )
    file_name = models.CharField(max_length=32)  # <dbkey><audit-year><version>.<pdf | xlsx>

    # Map to General/Audit
    audit = CompositeForeignKey(
        Audit,
        on_delete=models.DO_NOTHING,
        to_fields={
           'audit_year': 'audit_year',
           'dbkey': 'dbkey'
        },
        related_name='documents'
    )

    def __str__(self):
        return self.file_name
