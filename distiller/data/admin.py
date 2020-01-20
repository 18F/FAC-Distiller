from django.contrib import admin

from . import models


class AuditAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'audit_year', 'dbkey', 'audit_type', 'auditee_name',
        'material_weakness'
    )
    search_fields = ('dbkey', 'auditee_name', 'audit_year')


class CFDAAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'dbkey', 'audit_year', 'ein', 'cfda', 'federal_program_name',
        'cfda_program_name'
    )
    search_fields = ('dbkey', 'ein', 'cfda', 'federal_program_name')



admin.site.register(models.AssistanceListing)
admin.site.register(models.Audit, AuditAdmin)
admin.site.register(models.CFDA, CFDAAdmin)
