"""
This module implements an import of Assistance Listings from beta.sam.gov.

Assistance Listings include metadata about programs receiving grant funding.
"""

import csv
import json
from datetime import datetime

import smart_open
from django.db import transaction

from .. import models

# data.gov CSV file to import. For context, see:
# https://beta.sam.gov/data-services?domain=Assistance%20Listings%2Fdatagov
SOURCE_URL = 'https://s3.amazonaws.com/falextracts/Assistance%20Listings/datagov/AssistanceListings_DataGov_PUBLIC_CURRENT.csv'  # noqa

# Mapping of source CSV columns to model field names
COLUMN_MAPPING = {
    'Program Title': 'program_title',
    'Program Number': 'program_number',
    'Popular Name (020)': 'popular_name',
    'Federal Agency (030)': 'federal_agency',
    'Authorization (040)': 'authorization',
    'Objectives (050)': 'objectives',
    'Types of Assistance (060)': 'assistance_types',
    'Uses and Use Restrictions (070)': 'uses_restrictions',
    'Applicant Eligibility (081)': 'applicant_eligibility',
    'Beneficiary Eligibility (082)': 'beneficiary_eligibility',
    'Credentials/Documentation (083)': 'credentials_documentation',
    'Preapplication Coordination (091)': 'preapplication_coordination',
    'Application Procedures (092)': 'application_procedures',
    'Award Procedure (093)': 'award_procedure',
    'Deadlines (094)': 'deadlines',
    'Range of Approval/Disapproval Time (095)': 'approval_time',
    'Appeals (096)': 'appeals',
    'Renewals (097)': 'renewals',
    'Formula and Matching Requirements (101)': 'requirements',
    'Length and Time Phasing of Assistance (102)': 'assistance_period',
    'Reports (111)': 'reports',
    'Audits (112)': 'audits',
    'Records (113)': 'records',
    'Account Identification (121)': 'account_identification',
    'Obligations (122)': 'obligations',
    'Range and Average of Financial Assistance (123)': 'assistance_range',
    'Program Accomplishments (130)': 'program_accomplishments',
    'Regulations, Guidelines, and Literature (140)': 'regulations',
    'Regional or Local Office (151)': 'regional_local_office',
    'Headquarters Office (152)': 'headquarters_office',
    'Website Address (153)': 'website',
    'Related Programs (160)': 'related_programs',
    'Examples of Funded Projects (170)': 'funded_project_examples',
    'Criteria for Selecting Proposals (180)': 'selection_criteria',
    'Published Date': 'published_date',
    'Parent Shortname': 'parent_shortname',
    'URL': 'sam_gov_url',
    'Recovery': 'recovery',
}

SANITIZERS = {
    'recovery': lambda x: {'Yes': True, 'No': False}[x],
    'published_date': lambda x: datetime.strptime(x, '%b %d,%Y').date(),
    'authorization': json.loads,
    'credentials_documentation': json.loads,
    'preapplication_coordination': json.loads,
    'application_procedures': json.loads,
    'deadlines': json.loads,
    'requirements': json.loads,
    'assistance_period': json.loads,
    'reports': json.loads,
    'audits': json.loads,
    'program_accomplishments': json.loads,
    'regional_local_office': json.loads,
}


@transaction.atomic
def refresh():
    """
    Refresh the assistance listings table with the most recent data available.
    This job should be scheduled to refresh the table daily or weekly, and may
    be used to initialize a development database.
    """

    # DELETE rather than TRUNCATE so this transaction may be rolled back on
    # failure.
    models.AssistanceListing.objects.all().delete()

    assistance_listings = []

    # Use `smart_open` to stream CSV data from the source location.
    with smart_open.open(SOURCE_URL, encoding='latin-1') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            assistance_listing = models.AssistanceListing()
            for csv_column_name, model_field_name in COLUMN_MAPPING.items():
                value = row[csv_column_name]
                if model_field_name in SANITIZERS:
                    value = SANITIZERS[model_field_name](value)
                setattr(assistance_listing, model_field_name, value)
            assistance_listings.append(assistance_listing)

    models.AssistanceListing.objects.bulk_create(assistance_listings)
