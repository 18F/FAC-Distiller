"""
Load data from the Single Audit Database available at census.gov.

This module imports all columns defined in `key.xls`, available here:
https://harvester.census.gov/facdissem/PublicDataDownloads.aspx
"""

import csv
import io
import json
import os
import shutil
import sys
from datetime import datetime
from zipfile import ZipFile

from django.db import connection, transaction

from .. import models
from ...gateways import files


FAC_ROOT_URL = 'https://www2.census.gov/pub/outgoing/govs/singleaudit'

# In addition to the current year, the number of years to load.
# Note that 2018 has currently unparsable CFDA CSV.
FAC_PRIOR_YEARS = 2


# Register a pipe-delimited CSV dialect.
csv.register_dialect('piped', delimiter='|', quoting=csv.QUOTE_NONE)


def download_table(
    table_name: str,
    target_dir: str,
) -> None:
    """
    Download given table to specified location. Target files will be in the
    form: <target-root>/<table-name>/<timestamp>/<file-name>
    """

    table = FAC_TABLES[table_name]
    timestamp = datetime.now().isoformat().replace(':', '-')
    target_dir = os.path.join(target_dir, table_name, timestamp)

    for source_path in table['source_urls']:
        sys.stdout.write(f'Loading {source_path}...')
        sys.stdout.flush()
        file_name = os.path.basename(source_path)

        # Do the copy operation from source to destination
        try:
            with files.input_file(source_path, mode='rb') as src_file:
                if source_path.endswith('.zip'):
                    # We can't stream data out of a zip file, so load the
                    # entire thing into memory.
                    with ZipFile(io.BytesIO(src_file.read())) as zip_file:
                        for zip_entry in zip_file.namelist():
                            with zip_file.open(zip_entry) as zip_entry_file:
                                target_path = os.path.join(target_dir, zip_entry)
                                with files.output_file(target_path, mode='wb') as dest_file:
                                    shutil.copyfileobj(zip_entry_file, dest_file)

                else:
                    target_path = os.path.join(target_dir, file_name)
                    with files.output_file(target_path, mode='wb') as dest_file:
                        shutil.copyfileobj(src_file, dest_file)

        # If we can't open, the file probably doesn't exist. This will happen
        # with current audit year table dumps early in the year.
        except files.FileOpenFailure:
            sys.stdout.write('Load failure, skipping...\n')
            sys.stdout.flush()
            continue

        sys.stdout.write('Done!\n')
        sys.stdout.flush()


@transaction.atomic
def update_table(
    table_name: str,
    source_dir: str,
    delete_existing: bool = True,
    batch_size: int = 1_000,
) -> None:
    """
    Get the Distiller's database in sync with the latest from the Single Audit
    Database.
    """

    table = FAC_TABLES[table_name]

    if delete_existing:
        sys.stdout.write(f'Clearing {table_name} table... ')
        sys.stdout.flush()
        # Clear the existing table.
        # We could DELETE here rather than TRUNCATE, which would be safe
        # transactionally, but performance is very poor for the larger tables.
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {table["model"]._meta.db_table}')  # pylint: disable=W0212

    sys.stdout.write(f'Loading {table_name}...\n')
    sys.stdout.flush()

    root_dir = os.path.join(source_dir, table_name)
    dump_dirs = files.glob(f'{root_dir}/*/')

    if not dump_dirs:
        sys.stdout.write('No table dump exists. Exiting...\n')
        sys.stdout.flush()
        return

    most_recent_dump_dir = dump_dirs[-1]

    file_paths = files.glob(os.path.join(most_recent_dump_dir, '*'))
    for file_path in file_paths:
        sys.stdout.write(f'\tImporting {file_path}...')
        sys.stdout.flush()
        with files.input_file(file_path, encoding='latin-1') as csv_file:
            table["model"].objects.bulk_create(
                _yield_model_instances(csv_file, **table),
                batch_size=batch_size
            )

    sys.stdout.write('Done!\n')


def _sanitize_row(row, *, field_mapping, sanitizers, **_kwargs):
    sanitized_row = {}
    for csv_column_name, model_field_name in field_mapping.items():
        # Strip off excess whitespace and handle NULL values.
        value = row.get(csv_column_name)
        if value is not None:
            value = value.strip() or None
        if csv_column_name in sanitizers:
            sanitized_row[model_field_name] = sanitizers[csv_column_name](value)
        else:
            sanitized_row[model_field_name] = value

    return sanitized_row


def _yield_rows(reader, *, field_mapping, sanitizers, **_kwargs):
    while True:
        try:
            row = next(reader)
        except StopIteration:
            break
        except Exception as e:  # pylint: disable=W0703
            print('CSV parsing error.', e)
            continue
        sanitized_row = _sanitize_row(
            row,
            field_mapping=field_mapping,
            sanitizers=sanitizers
        )
        if sanitized_row is not None:
            yield sanitized_row


def _yield_model_instances(
    csv_file,
    *,
    model,
    field_mapping,
    sanitizers,
    file_reader,
    **_kwargs
):
    for row in _yield_rows(
        file_reader(csv_file),
        field_mapping=field_mapping,
        sanitizers=sanitizers
    ):
        yield model(**row)


def date_fmt(dt):
    if not dt:
        return None
    return datetime.strptime(dt, '%d-%b-%y')


def boolean(b):
    if not b:
        return None
    return {
        'Y': True,
        'N': False
    }.get(b.upper())


def _strip_rows(rows):
    for row in rows:
        if not row:
            continue
        yield row.strip()


def parse_fac_pipe_delimited(in_file):
    return csv.DictReader(in_file, dialect='piped')


def _fac_urls(file_prefix: str):
    # Get two prior years, plus this year (if the file exists).
    this_year = datetime.now().year
    return [
        os.path.join(FAC_ROOT_URL, f'{file_prefix}{year % 100:02d}.zip')
        for year in range(this_year, this_year - FAC_PRIOR_YEARS - 1, -1)
    ]



FAC_TABLES = {
    'assistancelisting': {
        'source_urls': [
            'https://s3.amazonaws.com/falextracts/Assistance%20Listings/datagov/AssistanceListings_DataGov_PUBLIC_CURRENT.csv'  # pylint: disable=C0301
        ],
        'model': models.AssistanceListing,
        'file_reader': csv.DictReader,
        'field_mapping': {
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
        },
        'sanitizers': {
            'Recovery': lambda x: {'Yes': True, 'No': False}[x],
            'Published Date': lambda x: datetime.strptime(x, '%b %d,%Y').date(),
            'Authorization (040)': json.loads,
            'Credentials/Documentation (083)': json.loads,
            'Preapplication Coordination (091)': json.loads,
            'Application Procedures (092)': json.loads,
            'Deadlines (094)': json.loads,
            'Formula and Matching Requirements (101)': json.loads,
            'Length and Time Phasing of Assistance (102)': json.loads,
            'Reports (111)': json.loads,
            'Audits (112)': json.loads,
            'Program Accomplishments (130)': json.loads,
            'Regional or Local Office (151)': json.loads,
        }
    },
    'audit': {
        'source_urls': _fac_urls('gen'),
        'model': models.Audit,
        'file_reader': parse_fac_pipe_delimited,
        'field_mapping': {
            'AUDITYEAR': 'audit_year',
            'DBKEY': 'dbkey',
            'TYPEOFENTITY': 'type_of_entity',
            'FYENDDATE': 'fy_end_date',
            'AUDITTYPE': 'audit_type',
            'PERIODCOVERED': 'period_covered',
            'NUMBERMONTHS': 'number_months',
            'EIN': 'ein',
            'MULTIPLEEINS': 'multiple_eins',
            'EINSUBCODE': 'ein_subcode',
            'DUNS': 'duns',
            'MULTIPLEDUNS': 'multiple_duns',
            'AUDITEENAME': 'auditee_name',
            'STREET1': 'street1',
            'STREET2': 'street2',
            'CITY': 'city',
            'STATE': 'state',
            'ZIPCODE': 'zipcode',
            'AUDITEECONTACT': 'auditee_contact',
            'AUDITEETITLE': 'auditee_title',
            'AUDITEEPHONE': 'auditee_phone',
            'AUDITEEFAX': 'auditee_fax',
            'AUDITEEEMAIL': 'auditee_email',
            'AUDITEEDATESIGNED': 'auditee_date_signed',
            'AUDITEENAMETITLE': 'auditee_name_title',
            'CPAFIRMNAME': 'cpa_firm_name',
            'CPASTREET1': 'cpa_street1',
            'CPASTREET2': 'cpa_street2',
            'CPACITY': 'cpa_city',
            'CPASTATE': 'cpa_state',
            'CPAZIPCODE': 'cpa_zipcode',
            'CPACONTACT': 'cpa_contact',
            'CPATITLE': 'cpa_title',
            'CPAPHONE': 'cpa_phone',
            'CPAFAX': 'cpa_fax',
            'CPAEMAIL': 'cpa_email',
            'CPADATESIGNED': 'cpa_date_signed',
            'COG_OVER': 'cog_over',
            'COGAGENCY': 'cog_agency',
            'OVERSIGHTAGENCY': 'oversight_agency',
            'TYPEREPORT_FS': 'typereport_fs',
            'SP_FRAMEWORK': 'sp_framework',
            'SP_FRAMEWORK_REQUIRED': 'sp_framework_required',
            'TYPEREPORT_SP_FRAMEWORK': 'typereport_sp_framework',
            'GOINGCONCERN': 'going_concern',
            'REPORTABLECONDITION': 'reportable_condition',
            'MATERIALWEAKNESS': 'material_weakness',
            'MATERIALNONCOMPLIANCE': 'material_noncompliance',
            'TYPEREPORT_MP': 'typereport_mp',
            'DUP_REPORTS': 'dup_reports',
            'DOLLARTHRESHOLD': 'dollar_threshold',
            'LOWRISK': 'low_risk',
            'REPORTABLECONDITION_MP': 'reportable_condition_mp',
            'MATERIALWEAKNESS_MP': 'material_weakness_mp',
            'QCOSTS': 'qcosts',
            'CYFINDINGS': 'cy_findings',
            'PYSCHEDULE': 'py_schedule',
            'TOTFEDEXPEND': 'tot_fed_expend',
            'DATEFIREWALL': 'date_firewall',
            'PREVIOUSDATEFIREWALL': 'previous_date_firewall',
            'REPORTREQUIRED': 'report_required',
            'MULTIPLE_CPAS': 'multiple_cpas',
            'AUDITOR_EIN': 'auditor_ein',
            'FACACCEPTEDDATE': 'fac_accepted_date',

            # These columns are not in 2019 exports:
            # 'CPAFOREIGN': 'cpa_foreign',
            # 'CPACOUNTRY': 'cpa_country',
        },
        'sanitizers': {
            'FYENDDATE': date_fmt,
            'AUDITEEDATESIGNED': date_fmt,
            'CPADATESIGNED': date_fmt,
            'DATEFIREWALL': date_fmt,
            'PREVIOUSDATEFIREWALL': date_fmt,
            'FACACCEPTEDDATE': date_fmt,
            'MULTIPLEEINS': boolean,
            'MULTIPLEDUNS': boolean,
            'MULTIPLE_CPAS': boolean,
            'SP_FRAMEWORK_REQUIRED': boolean,
            'GOINGCONCERN': boolean,
            'REPORTABLECONDITION': boolean,
            'MATERIALWEAKNESS': boolean,
            'MATERIALNONCOMPLIANCE': boolean,
            'DUP_REPORTS': boolean,
            'LOWRISK': boolean,
            'REPORTABLECONDITION_MP': boolean,
            'MATERIALWEAKNESS_MP': boolean,
            'QCOSTS': boolean,
            'CYFINDINGS': boolean,
            'PYSCHEDULE': boolean,
            'REPORTREQUIRED': boolean,
        }
    },
    'cfda': {
        'source_urls': _fac_urls('cfda'),
        'model': models.CFDA,
        'file_reader': parse_fac_pipe_delimited,
        'field_mapping': {
            'AUDITYEAR': 'audit_year',
            'DBKEY': 'dbkey',
            'EIN': 'ein',
            'CFDA': 'cfda_id',
            'AWARDIDENTIFICATION': 'award_identification',
            'RD': 'r_and_d',
            'LOANS': 'loans',
            'LOANBALANCE': 'loan_balance',
            'ARRA': 'arra',
            'FEDERALPROGRAMNAME': 'federal_program_name',
            'AMOUNT': 'amount',
            'CLUSTERNAME': 'cluster_name',
            'STATECLUSTERNAME': 'state_cluster_name',
            'PROGRAMTOTAL': 'program_total',
            'CLUSTERTOTAL': 'cluster_total',
            'DIRECT': 'direct',
            'PASSTHROUGHAWARD': 'pass_through_award',
            'PASSTHROUGHAMOUNT': 'pass_through_amount',
            'MAJORPROGRAM': 'major_program',
            'TYPEREPORT_MP': 'type_report_mp',
            'QCOSTS2': 'qcosts2',
            'FINDINGS': 'findings',
            'TYPEREQUIREMENT': 'type_requirement',
            'FINDINGREFNUMS': 'finding_ref_nums',
            'FINDINGSCOUNT': 'findings_count',
            'ELECAUDITSID': 'elec_audits_id',

            # These columns are not in 2019 exports:
            # 'OTHERCLUSTERNAME': 'other_cluster_name',
            # 'CFDAPROGRAMNAME': 'cfda_program_name',
        },
        'sanitizers': {
            'RD': boolean,
            'LOANS': boolean,
            'ARRA': boolean,
            'DIRECT': boolean,
            'PASSTHROUGHAWARD': boolean,
            'MAJORPROGRAM': boolean,
            'QCOSTS2': boolean,
        }
    },
    'finding': {
        'source_urls': _fac_urls('findings'),
        'model': models.Finding,
        'file_reader': parse_fac_pipe_delimited,
        'field_mapping': {
            'DBKEY': 'dbkey',
            'AUDITYEAR': 'audit_year',
            'ELECAUDITSID': 'elec_audits_id',
            'ELECAUDITFINDINGSID': 'elec_audit_findings_id',
            'FINDINGSREFNUMS': 'finding_ref_nums',
            'TYPEREQUIREMENT': 'type_requirement',
            'MODIFIEDOPINION': 'modified_opinion',
            'OTHERNONCOMPLIANCE': 'other_noncompliance',
            'MATERIALWEAKNESS': 'material_weakness',
            'SIGNIFICANTDEFICIENCY': 'significant_deficiency',
            'OTHERFINDINGS': 'other_findings',
            'QCOSTS': 'questioned_costs',
            'REPEATFINDING': 'repeat_finding',
            'PRIORFINDINGREFNUMS': 'prior_finding_ref_nums',
        },
        'sanitizers': {
            'TYPEREQUIREMENT': boolean,
            'MODIFIEDOPINION': boolean,
            'OTHERNONCOMPLIANCE': boolean,
            'MATERIALWEAKNESS': boolean,
            'SIGNIFICANTDEFICIENCY': boolean,
            'OTHERFINDINGS': boolean,
            'QCOSTS': boolean,
            'REPEATFINDING': boolean,
            'PRIORFINDINGREFNUMS': boolean,
        }
    },
    'findingtext': {
        'source_urls': _fac_urls('findingstext'),
        'model': models.FindingText,
        'file_reader': parse_fac_pipe_delimited,
        'field_mapping': {
            'SEQ_NUMBER': 'seq_number',
            'DBKEY': 'dbkey',
            'AUDITYEAR': 'audit_year',
            'FINDINGREFNUMS': 'finding_ref_nums',
            'TEXT': 'text',
            'CHARTSTABLES': 'charts_tables',
        },
        'sanitizers': {
            'CHARTSTABLES': boolean
        }
    },
    'captext': {
        'source_urls': _fac_urls('captext'),
        'model': models.CAPText,
        'file_reader': parse_fac_pipe_delimited,
        'field_mapping': {
            'SEQ_NUMBER': 'seq_number',
            'DBKEY': 'dbkey',
            'AUDITYEAR': 'audit_year',
            'FINDINGREFNUMS': 'finding_ref_nums',
            'TEXT': 'text',
            'CHARTSTABLES': 'charts_tables',
        },
        'sanitizers': {
            'CHARTSTABLES': boolean
        }
    }
}

FAC_TABLES_NAMES = tuple(FAC_TABLES.keys())
