"""
Load data from the Single Audit Database available at census.gov.

This module imports all columns defined in `key.xls`, available here:
https://harvester.census.gov/facdissem/PublicDataDownloads.aspx
"""

import csv
import sys
from datetime import datetime
from typing import Dict, Generator

import smart_open
from django.db import transaction

from .. import models


ROOT_URL = 'https://www2.census.gov/pub/outgoing/govs/singleaudit'


@transaction.atomic
def update_table(table_name: str):
    """
    Get the Distiller's database in sync with the latest from the Single Audit
    Database.

    NOTE: This currently only loads selected 2019 tables.
    """

    table = FAC_TABLES[table_name]

    sys.stdout.write(f'Importing {table["url"]}...')
    sys.stdout.flush()

    table["model"].objects.all().delete()

    with smart_open.open(table["url"], encoding='latin-1') as csv_file:
        table["model"].objects.bulk_create(
            _yield_model_instances(csv_file, **table),
            batch_size=1_000
        )

    sys.stdout.write('Done!\n')


def _sanitize_row(row, *, field_mapping, sanitizers, **kwargs):
    sanitized_row = {}
    for csv_column_name, model_field_name in field_mapping.items():
        # These are fixedwidth CSVs, so strip off excess whitespace and handle
        # NULL values.
        value = row[csv_column_name].strip() or None
        if csv_column_name in sanitizers:
            sanitized_row[model_field_name] = sanitizers[csv_column_name](value)
        else:
            sanitized_row[model_field_name] = value

    return sanitized_row


def _strip_rows(rows):
    for row in rows:
        if not row:
            continue
        yield row.strip()


def _yield_rows(reader, *, field_mapping, sanitizers, **kwargs):
    while True:
        try:
            row = next(reader)
        except StopIteration:
            break
        except Exception as e:
            print('CSV parsing error.', e)
            continue
        sanitized_row = _sanitize_row(
            row,
            field_mapping=field_mapping,
            sanitizers=sanitizers
        )
        if sanitized_row is not None:
            yield sanitized_row


def _yield_model_instances(csv_file, *, model, field_mapping, sanitizers, file_reader, **kwargs):
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
    return {
        'Y': True,
        'N': False
    }.get(b)


def parse_fac_csv(csv_file):
    """
    Parse a FAC-sources CSV.
    There are random empty lines in these files, so in addition to using the
    built-in CSV module, ignore empty lines.
    """
    return csv.DictReader(_strip_rows(csv_file))


def parse_findings_text_csv(csv_file) -> Generator[Dict[str, any], None, None]:
    """
    The FAC findings text table includes unescaped, multi-line text which a
    CSV parser is incapable of extracting. This function uses a regular
    expression to grab the data, and yields dict-like rows.
    """

    # Verify the header contains the expected columns
    first_line = next(csv_file)
    assert first_line.rstrip() == 'SEQ_NUMBER|DBKEY|AUDITYEAR|FINDINGREFNUMS|TEXT|CHARTSTABLES'

    # Iterate through the remainer of the file, collecting each row into a
    # dictionary, and yielding them.
    while True:
        row = {}

        # Get the first line - expected to look like:
        #            21,        66846,2019,2019-001
        try:
            line = next(csv_file).strip()
        except StopIteration:
            break

        # If the expected line isn't found, try going through the loop again.
        parts = line.split(',')
        if parts == ['']:
            continue

        assert len(parts) == 4, 'Unexpected field count'

        row['SEQ_NUMBER'] = parts[0].strip()
        row['DBKEY'] = parts[1].strip()
        row['AUDITYEAR'] = parts[2].strip()
        row['FINDINGREFNUMS'] = parts[3].strip()

        # Accumulate TEXT column lines until the CHARTSTABLES field is found.
        text_lines = []
        while True:
            line = next(csv_file).rstrip()

            # We determine the end of a findings text row by the presence of
            # the CHARTSTABLES value (Y/N) on its own line.
            if line in ('N', 'Y'):
                row['CHARTSTABLES'] = line

                # There's always an empty line at the end of each row; skip it
                # and process the next row.
                next(csv_file)
                break

            text_lines.append(line)

        row['TEXT'] = '\n'.join(text_lines)

        yield row


FAC_TABLES = {
    'audit': {
        # 'url': f'{ROOT_URL}/gen{year}.zip',
        'url': '/Users/dan/src/10x/fac-distiller/imports/gen19.txt',
        'model': models.Audit,
        'file_reader': parse_fac_csv,
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
        # 'url': f'{ROOT_URL}/cfda{year}.zip',
        'url': '/Users/dan/src/10x/fac-distiller/imports/cfda19.txt',
        'model': models.CFDA,
        'file_reader': parse_fac_csv,
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
        'url': '/Users/dan/src/10x/fac-distiller/imports/findings19.txt',
        # 'url': f'{ROOT_URL}/findings{year}.zip',
        'model': models.Finding,
        'file_reader': parse_fac_csv,
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
        # 'url': f'{ROOT_URL}/findingstext19.zip',
        'url': '/Users/dan/src/10x/fac-distiller/imports/findingstext19.txt',
        'model': models.FindingText,
        'file_reader': parse_findings_text_csv,
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
    #     'url': f'{ROOT_URL}/notes{year}.zip',
    #     'model': models.Note,
    #     'field_mapping': [],
    #     'sanitizers': {}
    # }, {
    #     'url': f'{ROOT_URL}/captext{year}.zip',
    #     'model': models.CAPText,
    #     'field_mapping': [],
    #     'sanitizers': {}
    # }, {
    #     'url': f'{ROOT_URL}/revisions{year}.zip',
    #     'model': models.Revision,
    #     'field_mapping': [],
    #     'sanitizers': {}
    # }
}

FAC_TABLES_NAMES = tuple(FAC_TABLES.keys())
