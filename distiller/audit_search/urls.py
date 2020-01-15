from django.urls import path

from .views import (offer_download_of_agency_specific_csv,
                    search_by_agency, show_agency_level_summary)


app_name = 'distiller.audit_search'

urlpatterns = [
    path('', search_by_agency, name='home'),
    path('get-single-audits-by-agency/', show_agency_level_summary, name='show_relevant_audits'),
    path('generate-a-csv/', offer_download_of_agency_specific_csv, name='prompt_to_save_csv'),
]
