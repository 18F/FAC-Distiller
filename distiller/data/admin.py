from django.contrib import admin

from . import models


class AuditAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'audit_year', 'dbkey', 'audit_type', 'auditee_name',
        'material_weakness', 'ein'
    )
    search_fields = ('dbkey', 'auditee_name', 'audit_year', 'ein')


class CFDAAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'dbkey', 'audit_year', 'ein', 'cfda', 'federal_program_name',
        'cfda_program_name'
    )
    search_fields = (
        'dbkey', 'ein', 'cfda', 'federal_program_name', 'federal_agency'
    )


class AssistanceListingAdmin(admin.ModelAdmin):
    list_filter = (
        'federal_agency',
    )


class FindingAdmin(admin.ModelAdmin):
    list_display = (
        'audit_year', 'dbkey', 'finding_ref_nums'
    )
    raw_id_fields = ('elec_audits',)



admin.site.register(models.AssistanceListing, AssistanceListingAdmin)
admin.site.register(models.Audit, AuditAdmin)
admin.site.register(models.CFDA, CFDAAdmin)
admin.site.register(models.Finding, FindingAdmin)