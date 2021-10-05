from django.contrib import admin
from ereturns.rit.models import (
    RitFeatures, RitSupervision,
    RitManagement
)


admin.site.register(RitFeatures)
admin.site.register(RitSupervision)

@admin.register(RitManagement)
class RitManagementAdmin(admin.ModelAdmin):
    fieldsets = (
        (("Rit Management"),
         {"fields": ("file_type",
                     "rit",
                     "department",
                     "file",
                     "uploaded_by",
                     "upload_time",
                     "version"
                     )}),
    )
    list_display = ["file_type", "rit", "file"]



