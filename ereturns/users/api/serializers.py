from django.contrib.auth import get_user_model
from rest_framework import serializers
from ereturns.common.library import ChoiceField
from ereturns.users.constants import Status

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "name"]


class UserSerializer(serializers.ModelSerializer):
    report_type = serializers.SerializerMethodField()
    financial_institute_type = serializers.SerializerMethodField()
    financial_institute = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    status = ChoiceField(choices=Status.Status)

    class Meta:
        model = User
        fields = ["id", "username", "name", "report_type", "financial_institute_type",
                  "financial_institute", "branch", "status", "email", "designation", "department",
                  "mobile", "phone", "last_login", "is_active", "is_active",
                  "change_approved_by", "approved_time", "approved_by", "password_reset_time",
                  "last_password_update_time", "first_approved_by", "second_approved_by",
                  "date_joined","password_updated_by", "random_string"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "id"}
        }

    def get_report_type(self, obj):
        if obj.report_type:
            return f"{obj.report_type.name}"

    def get_financial_institute_type(self, obj):
        fi_type = {
            "id": obj.financial_institute_type.id,
            "name": obj.financial_institute_type.name,
        }
        return fi_type

    def get_financial_institute(self, obj):
        # return f"{obj.financial_institute.name}"
        fi = {
            "id": obj.financial_institute.id,
            "name": obj.financial_institute.name,
        }
        return fi

    def get_branch(self, obj):
        # return f"{obj.branch.name}"
        branch = {
            "id": obj.branch.id,
            "name": obj.branch.name,
        }
        return branch

    def get_department(self, obj):
        # return f"{obj.department.name}"
        department = {
            "id": obj.department.id,
            "name": obj.department.name,
        }
        return department
