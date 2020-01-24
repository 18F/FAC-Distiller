from django.urls import path

from .views import (offer_download_of_agency_specific_csv, scrape_audits,
                    single_audit_search, show_agency_level_summary, view_audit,
                    view_finding)


app_name = 'distiller.audit_search'

urlpatterns = [
    path('', single_audit_search, name='home'),
    path('<int:audit_id>/', view_audit, name='view_audit'),
    path('findings/<int:finding_id>/', view_finding, name='view_finding'),
    path('', scrape_audits, name='scrape_audits'),
    path('get-single-audits-by-agency/', show_agency_level_summary, name='show_relevant_audits'),
    path('generate-a-csv/', offer_download_of_agency_specific_csv, name='prompt_to_save_csv'),
]
