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
        'elec_audits_id', 'dbkey', 'audit_year', 'ein', 'cfda_id',
        'federal_program_name', 'cfda_program_name'
    )
    raw_id_fields = ('cfda',)


class AssistanceListingAdmin(admin.ModelAdmin):
    list_filter = (
        'federal_agency',
    )


class FindingAdmin(admin.ModelAdmin):
    list_display = (
        'audit_year', 'dbkey', 'finding_ref_nums'
    )
    raw_id_fields = ('elec_audits',)


class FindingTextAdmin(admin.ModelAdmin):
    list_display = (
        'seq_number', 'dbkey', 'audit_year', 'finding_ref_nums', 'charts_tables'
    )


class CAPTextAdmin(admin.ModelAdmin):
    list_display = (
        'seq_number', 'dbkey', 'audit_year', 'finding_ref_nums', 'charts_tables'
    )


class PDFExtractAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'audit_year', 'dbkey', 'finding_ref_nums'
    )


class ETLLogAdmin(admin.ModelAdmin):
    list_display = (
        'created', 'operation', 'target'
    )


admin.site.register(models.AssistanceListing, AssistanceListingAdmin)
admin.site.register(models.Audit, AuditAdmin)
admin.site.register(models.CFDA, CFDAAdmin)
admin.site.register(models.Finding, FindingAdmin)
admin.site.register(models.FindingText, FindingTextAdmin)
admin.site.register(models.CAPText, CAPTextAdmin)
admin.site.register(models.PDFExtract, PDFExtractAdmin)
admin.site.register(models.ETLLog, ETLLogAdmin)
