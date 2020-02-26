from django.contrib import admin
from django.urls import path, include

# Register apscheduler jobs
import distiller.data.jobs
import distiller.fac_scraper.jobs



admin.site.site_header = "FAC Distiller Admin"
admin.site.site_title = "FAC Distiller Admin Portal"
admin.site.index_title = "Welcome to FAC Distiller Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('distiller.audit_search.urls', namespace='audit_search')),
]
