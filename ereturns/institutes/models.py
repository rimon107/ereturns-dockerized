from django.db import models
from django.utils.translation import gettext_lazy as _


class Division(models.Model):
    name = models.CharField(_("Division"), blank=True, max_length=255)

    def __str__(self):
        return f"{self.name}"


class District(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(_("District"), blank=True, max_length=255)

    def __str__(self):
        return f"{self.name}"


class Upazila(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(_("Upazila"), blank=True, max_length=255)

    def __str__(self):
        return f"{self.name}"


class FinancialInstituteType(models.Model):
    code = models.CharField(_("code"), blank=True, max_length=255)
    name = models.CharField(_("financial institute type"), blank=True, max_length=255)

    def __str__(self):
        return f"{self.name}"


class FinancialInstitute(models.Model):
    code = models.CharField(_("code"), blank=True, max_length=255)
    name = models.CharField(_("financial institute"), blank=True, max_length=255)
    financial_institute_type = models.ForeignKey(
        FinancialInstituteType,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name}"


class Branch(models.Model):
    code = models.CharField(_("code"), blank=True, max_length=255)
    name = models.CharField(_("branch"), blank=True, max_length=255)
    financial_institute_type = models.ForeignKey(
        FinancialInstituteType,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    financial_institute = models.ForeignKey(
        FinancialInstitute,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    upazila = models.ForeignKey(Upazila, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Department(models.Model):
    code = models.CharField(_("code"), blank=True, max_length=255)
    name = models.CharField(_("department"), blank=True, max_length=255)
    financial_institute_type = models.ForeignKey(
        FinancialInstituteType,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    financial_institute = models.ForeignKey(
        FinancialInstitute,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name}"


class ReportType(models.Model):
    name = models.CharField(_("Report type"), blank=True, max_length=255)

    def __str__(self):
        return f"{self.name}"
