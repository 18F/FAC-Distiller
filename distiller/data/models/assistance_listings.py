from django.db import models
from django.contrib.postgres.fields import JSONField


class AssistanceListingManager(models.Manager):
    def with_prefix(self, prefix):
        return self.filter(
            program_number__startswith=prefix
        )

    def distinct_agencies(self, agency_prefix):
        return self.with_prefix(agency_prefix).distinct(
            'federal_agency').values_list('federal_agency', flat=True)

    def get_cfda_nums_for_agency(self, federal_agency: str):
        return list(self.filter(federal_agency=federal_agency).values_list(
            'program_number', flat=True
        ))


class AssistanceListing(models.Model):
    """
    Assistance listings from sam.gov.
    We load this so we may map CFDA numbers (program_number) to federal
    agencies (federal_agency).
    """

    objects = AssistanceListingManager()

    program_number = models.CharField(
        primary_key=True,
        # We make this 64 rather than 6 to accomodate invalid foreign key
        # references to this table (see: CFDA table).
        max_length=64,
        help_text='Program Number'
    )
    program_title = models.TextField(help_text='Program Title')
    popular_name = models.TextField(
        help_text='Popular Name (020)',
        blank=True,
        null=True,
    )
    federal_agency = models.TextField(help_text='Federal Agency (030)')
    authorization = JSONField(help_text='Authorization (040)')
    objectives = models.TextField(help_text='Objectives (050)')
    assistance_types = models.TextField(
        help_text='Types of Assistance (060)'
    )
    uses_restrictions = models.TextField(
        help_text='Uses and Use Restrictions (070)'
    )
    applicant_eligibility = models.TextField(
        help_text='Applicant Eligibility (081)'
    )
    beneficiary_eligibility = models.TextField(
        help_text='Beneficiary Eligibility (082)'
    )
    credentials_documentation = JSONField(
        help_text='Credentials/Documentation (083)'
    )
    preapplication_coordination = JSONField(
        help_text='Preapplication Coordination (091)'
    )
    application_procedures = JSONField(
        help_text='Application Procedures (092)'
    )
    award_procedure = models.TextField(
        help_text='Award Procedure (093)')
    deadlines = JSONField(help_text='Deadlines (094)')
    approval_time = models.TextField(
        help_text='Range of Approval/Disapproval Time (095)'
    )
    appeals = models.TextField(help_text='Appeals (096)')
    renewals = models.TextField(help_text='Renewals (097)')
    requirements = JSONField(
        help_text='Formula and Matching Requirements (101)'
    )
    assistance_period = JSONField(
        help_text='Length and Time Phasing of Assistance (102)',
        null=True
    )
    reports = JSONField(help_text='Reports (111)')
    audits = JSONField(help_text='Audits (112)')
    records = models.TextField(
        help_text='Records (113)',
        blank=True,
        null=True,
    )
    account_identification = models.TextField(
        help_text='Account Identification (121)'
    )
    obligations = models.TextField(help_text='Obligations (122)')
    assistance_range = models.TextField(
        help_text='Range and Average of Financial Assistance (123)',
        blank=True,
        null=True,
    )
    program_accomplishments = JSONField(
        help_text='Program Accomplishments (130)'
    )
    regulations = models.TextField(
        help_text='Regulations, Guidelines, and Literature (140)'
    )
    regional_local_office = JSONField(
        help_text='Regional or Local Office (151)'
    )
    headquarters_office = models.TextField(
        help_text='Headquarters Office (152)'
    )
    website = models.URLField(
        help_text='Website Address (153)',
        blank=True,
        null=True,
    )
    related_programs = models.TextField(
        help_text='Related Programs (160)',
        blank=True,
        null=True,
    )
    funded_project_examples = models.TextField(
        help_text='Examples of Funded Projects (170)',
        blank=True,
        null=True,
    )
    selection_criteria = models.TextField(
        help_text='Criteria for Selecting Proposals (180)'
    )
    published_date = models.DateField(help_text='Published Date')
    parent_shortname = models.CharField(
        max_length=8,
        help_text='Parent Shortname',
        blank=True,
        null=True,
    )
    sam_gov_url = models.URLField(help_text='URL')
    recovery = models.BooleanField(help_text='Recovery')

    def __str__(self):
        return f'{self.program_number} {self.program_title}'
