"""
Views for audit clearinghouse search interface.
"""

from io import StringIO

from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd

from distiller.data.etls import selenium_scraper
from .forms import AGENCIES_BY_PREFIX, AgencySelectionForm


def search_by_agency(request):
    # Form submissions are with POST, but filtering on parent agency is handled
    # with GET.
    form = AgencySelectionForm(request.POST or request.GET)

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

    return render(request, 'distiller/index.html', {'form': form})


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
    return render(request, 'distiller/results.html', highlights)
