import json

from django.db import models

from compositefk.fields import CompositeForeignKey

from .single_audit_db import Audit


class PDFExtract(models.Model):
    """
    PDF extract, per audit number.
    Attempt to extract as much data from the PDF as we can.
    """
    class Meta:
        verbose_name_plural = 'PDF extracts'
        indexes = [
           models.Index(fields=['audit_year', 'dbkey']),
        ]

    # Use these fields to link tables- 4 digits
    audit_year = models.DecimalField(
        max_digits=4,
        decimal_places=0,
        help_text='Audit Year and DBKEY (database key) combined make up the primary key.'
    )
    # Use these fields to link tables- 1-6 digits
    dbkey = models.CharField(
        max_length=6,
        help_text='Audit Year and DBKEY (database key) combined make up the primary key.'
    )
    # Map to General/Audit
    audit = CompositeForeignKey(
        Audit,
        on_delete=models.DO_NOTHING,
        to_fields={
           'audit_year': 'audit_year',
           'dbkey': 'dbkey'
        },
        related_name='pdf_extracts'
    )

    finding_ref_nums = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        help_text='Findings Reference Numbers'
    )
    finding_text = models.JSONField(help_text='Extracted PDF finding')
    cap_text = models.JSONField(help_text='Extracted PDF corrective action plan')
    last_updated = models.DateField(help_text='Last Updated')

    def __str__(self):
        return f'PDF extract of {self.audit}: {self.finding_ref_nums}'

    def finding_to_dict(self):
        return json.loads(self.finding_text)

    def cap_to_dict(self):
        return json.loads(self.cap_text)
