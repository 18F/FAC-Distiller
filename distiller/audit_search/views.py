"""
Views for audit clearinghouse search interface.
"""

import csv
import itertools
from datetime import datetime
from io import StringIO

from django.core.paginator import Paginator
from django.http import (
    Http404, HttpResponse, HttpResponseBadRequest, StreamingHttpResponse
)

import pandas as pd
from django.shortcuts import render

from distiller.data.constants import AGENCIES_BY_PREFIX
from distiller.data.etls import selenium_scraper
from distiller.data import models
from .forms import AgencySelectionForm


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def get_load_status():
    last_load = models.ETLLog.objects.get_most_recent_load_table()
    last_crawl = models.ETLLog.objects.get_most_recent_document_crawl()
    return {
        'last_load_job_run_time': last_load.created if last_load else None,
        'last_crawl_job_run_time': last_crawl.created if last_crawl else None,
    }


def single_audit_search(request):
    form = AgencySelectionForm(request.GET or None)

    page = None
    finding_texts = None
    if form.is_valid():
        audits = models.Audit.objects.filter_dates(
            audit_year=form.cleaned_data['audit_year'],
            start_date=form.cleaned_data['start_date'],
            end_date=form.cleaned_data['end_date'],
        ).prefetch_related(
            'finding_texts',
            'finding_texts__findings',
            'finding_texts__findings__elec_audits',
            'finding_texts__cap_texts',
            'documents',
        )

        # If specified, filter by sub-agency name. To do this, we need to query
        # for matching CFDA numbers first.
        if form.cleaned_data['sub_agency']:
            cfdas = models.AssistanceListing.objects.get_cfda_nums_for_agency(
                form.cleaned_data['sub_agency']
            )
            audits = audits.filter_cfda_list(cfdas)

        # Otherwise, filter by parent agency prefix
        else:
            audits = audits.filter_cfda_prefix(form.cleaned_data['agency'])

        # If specified, only include results where the parent agency is
        # cognizant/oversight.
        if form.cleaned_data['agency_cog_oversight']:
            audits = audits.filter_cognizant_oversight_agency(
                form.cleaned_data['agency']
            )

        if form.cleaned_data['sort']:
            prefix = '-' if form.cleaned_data.get('order') == 'asc' else ''
            audits = audits.order_by(f'{prefix}{form.cleaned_data["sort"]}')

        audits = audits.filter_num_findings(require_findings=form.cleaned_data['findings'])

        page = Paginator(audits, 25).get_page(form.cleaned_data['page'] or 1)

        finding_texts_set = set()
        for audit in page.object_list:
            finding_texts_set.update(audit.finding_texts.all())

        finding_texts = sorted(
            finding_texts_set,
            key=lambda f: (f.audit_year, f.dbkey, f.finding_ref_nums)
        )

        if form.cleaned_data['fmt'] == 'csv':
            writer = csv.writer(Echo())
            rows = itertools.chain(
                (EXPORT_COLUMNS,),
                audits.values_list(*EXPORT_COLUMNS),
            )
            response = StreamingHttpResponse(
                (writer.writerow(row) for row in rows),
                content_type="text/csv"
            )
            response['Content-Disposition'] = 'attachment; filename="fac-distiller-search-results.csv"'
            return response

    return render(request, 'audit_search/search.html', {
        'form': form,
        'page': page,
        'finding_texts': finding_texts,
        'table_last_updated': datetime.now(),
        'table_loading_error': True,
        **get_load_status(),
    })

EXPORT_COLUMNS = [
    'audit_year',
    'dbkey',
    'type_of_entity',
    'fy_end_date',
    'audit_type',
    'period_covered',
    'number_months',
    'ein',
    'multiple_eins',
    'ein_subcode',
    'duns',
    'multiple_duns',
    'auditee_name',
    'street1',
    'street2',
    'city',
    'state',
    'zipcode',
    'auditee_contact',
    'auditee_title',
    'auditee_phone',
    'auditee_fax',
    'auditee_email',
    'auditee_date_signed',
    'auditee_name_title',
    'cpa_firm_name',
    'auditor_ein',
    'cpa_street1',
    'cpa_street2',
    'cpa_city',
    'cpa_state',
    'cpa_zipcode',
    'cpa_contact',
    'cpa_title',
    'cpa_phone',
    'cpa_fax',
    'cpa_email',
    'cpa_date_signed',
    'multiple_cpas',
    'cog_over',
    'cog_agency',
    'oversight_agency',
    'typereport_fs',
    'sp_framework',
    'sp_framework_required',
    'typereport_sp_framework',
    'going_concern',
    'reportable_condition',
    'material_weakness',
    'material_noncompliance',
    'typereport_mp',
    'dup_reports',
    'dollar_threshold',
    'low_risk',
    'reportable_condition_mp',
    'material_weakness_mp',
    'qcosts',
    'cy_findings',
    'py_schedule',
    'tot_fed_expend',
    'date_firewall',
    'previous_date_firewall',
    'report_required',
    'fac_accepted_date',
    'cpa_foreign',
    'cpa_country',
]


def view_audit(request, audit_id):
    audit = models.Audit.objects.get(pk=audit_id)
    #audit = access.get_audit(audit_id)

    if audit is None:
        raise Http404('Audit not found.')

    return render(request, 'audit_search/audit.html', {
        'audit': audit
    })


def view_finding(request, finding_id):
    finding = models.Finding.objects.get(pk=finding_id)

    if finding is None:
        raise Http404('Finding not found.')

    return render(request, 'audit_search/finding.html', {
        'finding': finding
    })


def scrape_audits(request):
    """
    Run the Selenium scraper on-demand for given agency/sub-agency.
    """

    form = AgencySelectionForm(request.POST or None)

    # If form is valid, return results.
    if request.method == 'POST' and form.is_valid():
        selenium_scraper.download_files_from_fac(
            agency_prefix=form.cleaned_data['agency'],
            subagency_extension=form.cleaned_data['sub_agency'],
        )
        return HttpResponse(
            "Your download has completed.",
            content_type="text/plain"
        )

    raise HttpResponseBadRequest()


def _get_findings(agency_df):
    """
    Args:
        A dataframe of agency data, currently derived from genXX.txt.

    Returns:
        A dataframe of findings, or 'None'.

    Room for improvement:
        Modify this function to retrieve the cross-referenced findings instead
        of just 'Y/N'.
    """

    try:
        findings_df = agency_df.loc[agency_df['CYFINDINGS'] == 'Y']
        return findings_df

    except:
        # @todo: Figure out what exception to actually raise here.
        raise Exception(" Error generating findings dataframe.")


def _get_number_of_findings(agency_df):
    """
    Args:
        agency_df: A dataframe of agency data, currently derived from genXX.txt.

    Returns:
        An integer, or 'None'.
    """

    try:
        findings_df = _get_findings(agency_df)
        return len(findings_df.index)

    except:
        raise Exception(" Error getting number of findings.")


def _filter_general_table_by_agency(agency_prefix, filename="gen18.txt"):
    actual_filename = selenium_scraper.FILES_DIRECTORY + '/' + filename

    # Not using the index for anything, so let's leave it arbitrary for now.
    df = pd.read_csv(actual_filename, low_memory=False, encoding='latin-1')

    agency_df = df.loc[df['COGAGENCY'] == agency_prefix]

    return agency_df


# @todo: clean up the naming here.
def _generate_csv_download(dataframe, results_filename='agency-specific-results.csv'):
    # Use a buffer so we can prompt the user to download the file.
    new_csv = StringIO()

    dataframe.to_csv(new_csv, encoding='utf-8', index=False)
    # Rewind the buffer so we don't get a zero-length error.
    new_csv.seek(0)

    response = HttpResponse(new_csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % results_filename

    return response


def offer_download_of_agency_specific_csv(
    request, agency_prefix=selenium_scraper.DEPT_OF_TRANSPORTATION_PREFIX
):
    agency_df = _filter_general_table_by_agency(agency_prefix)

    response = _generate_csv_download(agency_df)

    return response


def _derive_agency_highlights(agency_prefix, filename='gen18.txt'):
    agency_df = _filter_general_table_by_agency(agency_prefix)

    highlights = {  # or "overview"
        'agency_prefix': agency_prefix,
        'agency_names': AGENCIES_BY_PREFIX,
        'filename': filename,
        'results': {
            'cognizant_sum': len(agency_df.index),
            'findings': _get_number_of_findings(agency_df),
        }
        # 'cog_or_oversight': [_____]  # @todo: Think through and add this later.
    }

    return highlights


def show_agency_level_summary(request):
    agency_prefix = request.POST['agency']
    if agency_prefix not in AGENCIES_BY_PREFIX:
        raise ValueError("That doesn't seem to be a valid federal agency prefix.")

    highlights = _derive_agency_highlights(agency_prefix)
    return render(request, 'audit_search/results.html', highlights)
