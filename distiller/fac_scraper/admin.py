from django.contrib import admin

from . import models


class FacDocumentAdmin(admin.ModelAdmin):
    search_fields = ('file_name',)
    list_filter = (
        'audit_year',
        'audit__cfda__cfda__federal_agency',
    )


admin.site.register(models.FacDocument, FacDocumentAdmin)
