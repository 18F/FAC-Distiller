from django.urls import path

from .views import (download_files_from_fac,
                    offer_download_of_agency_specific_csv,
                    prompt_for_agency_name, show_agency_level_summary)


app_name = 'distiller.audit_search'

urlpatterns = [
    path('', prompt_for_agency_name, name='home'),
    path('get-single-audits-by-agency/', show_agency_level_summary, name='show_relevant_audits'),
    path('generate-a-csv/', offer_download_of_agency_specific_csv, name='prompt_to_save_csv'),
    path('download-single-audits/', download_files_from_fac, name='download_single_audit_files')
]
