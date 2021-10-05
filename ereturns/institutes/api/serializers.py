from rest_framework import serializers

from ereturns.institutes.models import (
    Division, District, Upazila, FinancialInstitute, Branch, Department
)


class DivisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Division
        fields = ["id", "name"]


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ["id", "name"]


class UpazilaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Upazila
        fields = ["id", "name"]


class FinancialInstituteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialInstitute
        fields = ["id", "code", "name"]


class BaseBranchSerializer(serializers.ModelSerializer):
    # fi = FinancialInstituteSerializer(many=False, read_only=True)

    class Meta:
        model = Branch
        fields = ["id", "code", "name"]


class BranchSerializer(serializers.ModelSerializer):
    financial_institute = FinancialInstituteSerializer(many=False, read_only=True)
    division = DivisionSerializer(many=False, read_only=True)
    district = DistrictSerializer(many=False, read_only=True)
    upazila = UpazilaSerializer(many=False, read_only=True)

    class Meta:
        model = Branch
        fields = ["id", "code", "name", "financial_institute",
                  "division", "district", "upazila"]


class DepartmentSerializer(serializers.ModelSerializer):
    # fi = FinancialInstituteSerializer(many=False, read_only=True)

    class Meta:
        model = Department
        fields = ["id", "code", "name"]
