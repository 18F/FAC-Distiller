from django.contrib import admin

from . import models


class FacDocumentAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.FacDocument, FacDocumentAdmin)
