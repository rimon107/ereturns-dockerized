from django.contrib import admin

from ereturns.institutes.models import (
    Division, District, Upazila,
    FinancialInstitute, Branch, ReportType,
    FinancialInstituteType, Department
)


admin.site.register(Division)
admin.site.register(District)
admin.site.register(Upazila)
admin.site.register(FinancialInstituteType)
admin.site.register(FinancialInstitute)
admin.site.register(ReportType)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "financial_institute"]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "branch", "financial_institute"]
