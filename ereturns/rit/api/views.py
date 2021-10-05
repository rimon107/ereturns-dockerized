from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ereturns.institutes.api.serializers import DepartmentSerializer
from ereturns.institutes.models import Department, Branch
from ereturns.rit.api.serializers import (
    RitFeaturesSerializer, RitSupervisionSerializer, RitSupervisionReadSerializer,
    BaseRitFeaturesSerializer, RitManagementSerializer, RitNonReportingBranchSerializer
)
from ereturns.rit.constants import RitFrequency, FileType
from ereturns.rit.models import (
    RitFeatures, RitSupervision, RitManagement
)
from ereturns.common.library import ChoiceField


class RitFrequencyViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = BaseRitFeaturesSerializer
    queryset = RitFeatures.objects.all()

    @action(detail=False, methods=["GET"])
    def frequency(self, request):
        serializer = ChoiceField(choices=RitFrequency.Frequency)
        return Response(serializer.choices)


class RitFeaturesViewSet(GenericViewSet):
    serializer_class = RitManagementSerializer
    queryset = RitFeatures.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=["GET"])
    def features(self, request):
        frequency_id = self.request.GET.get('frequency_id')
        if frequency_id:
            features = RitFeatures.objects.filter(frequency=frequency_id).values().order_by("code")
            serializer = BaseRitFeaturesSerializer(features, many=True)
        else:
            features = RitFeatures.objects.select_related("department").order_by("code")
            serializer = RitFeaturesSerializer(features, many=True)
        return Response(serializer.data)


class RitUploadStatusViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RitSupervisionReadSerializer
    queryset = RitSupervision.objects.all()
    lookup_field = "id"


class RitSupervisionViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RitSupervisionSerializer
    queryset = RitSupervision.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=["POST"])
    def upload(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RitDownloadViewSet(GenericViewSet):
    serializer_class = RitManagementSerializer
    queryset = RitManagement.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=["GET"])
    def departments(self, request):
        depts = self.queryset.filter(file_type=FileType.RIT).values_list("department", flat=True)
        departments = Department.objects.filter(id__in=depts).values()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def files(self, request):
        department_id = self.request.GET.get('department_id')
        if department_id:
            files = self.queryset.filter(department_id=department_id, file_type=FileType.RIT)
            serializer = RitManagementSerializer(files, many=True, context={"request": request})
        else:
            files = self.queryset.filter(file_type__in=[FileType.REFERENCE,
                                                        FileType.USER_MANUAL,
                                                        FileType.USER_REGISTRATION_FORM]
                                         ).order_by("file_type")
            serializer = RitManagementSerializer(files, many=True, context={"request": request})
        return Response(serializer.data)


class RitReportViewSet(GenericViewSet):
    serializer_class = RitSupervisionSerializer
    queryset = RitSupervision.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=["GET"], url_path="upload-status/base-date-wise")
    def upload_status_base_date_wise(self, request):
        rit_id = self.request.GET.get('rit_id')
        fi_id = self.request.GET.get('fi_id')
        base_date = self.request.GET.get('base_date')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if rit_id and fi_id and base_date:
            query = {
                "rit_id": rit_id,
                "financial_institute_id": fi_id,
                "base_date__date": base_date
            }

            if date_from:
                query["upload_time__date__gte"] = date_from

            if date_to:
                query["upload_time__date__lte"] = date_to

            result = self.queryset.filter(**query).select_related("rit", "financial_institute_type",
                                                                  "financial_institute", "branch", "department",
                                                                  "uploaded_by").order_by("rit_id")
            serializer = RitSupervisionSerializer(result, many=True, context={"request": request})
            return Response(serializer.data)
        else:
            data = {}
            if not fi_id:
                data["fi_name"] = [
                        "This field is required."
                    ]
            if not rit_id:
                data["rit_name"] = [
                        "This field is required."
                    ]
            if not base_date:
                data["base_date"] = [
                        "This field is required."
                    ]
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

    @action(detail=False, methods=["GET"], url_path="upload-status/bank-wise")
    def upload_status_bank_wise(self, request):
        rit_id = self.request.GET.get('rit_id')
        fi_id = self.request.GET.get('fi_id')
        date_from = self.request.GET.get('date_from')

        if rit_id and fi_id and date_from:
            query = {
                "rit_id": rit_id,
                "financial_institute_id": fi_id,
                "upload_time__date__gte": date_from
            }

            result = self.queryset.filter(**query).select_related("rit", "financial_institute_type",
                                                                  "financial_institute", "branch", "department",
                                                                  "uploaded_by").order_by("rit_id")
            serializer = RitSupervisionSerializer(result, many=True, context={"request": request})
            return Response(serializer.data)
        else:
            data = {}
            if not fi_id:
                data["fi_name"] = [
                    "This field is required."
                ]
            if not rit_id:
                data["rit_name"] = [
                    "This field is required."
                ]
            if not date_from:
                data["date_from"] = [
                    "This field is required."
                ]
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

    @action(detail=False, methods=["GET"], url_path="upload-status/non-reporting-branch")
    def upload_status_non_reporting_branch(self, request):
        rit_id = self.request.GET.get('rit_id')
        fi_id = self.request.GET.get('fi_id')
        base_date = self.request.GET.get('base_date')

        if rit_id and fi_id and base_date:
            query = {
                "rit_id": rit_id,
                "financial_institute_id": fi_id,
                "base_date__date": base_date
            }

            reporting_branches = Q(id__in=self.queryset.filter(**query).values_list("branch__id", flat=True))
            fi_branches = Branch.objects.filter(financial_institute_id=fi_id)
            non_reporting_branches = fi_branches.filter(~reporting_branches).values_list("id", flat=True)
            User = get_user_model()
            users = User.objects.filter(branch__id__in=non_reporting_branches)
            serializer = RitNonReportingBranchSerializer(users, many=True)
            return Response(serializer.data)
        else:
            data = {}
            if not fi_id:
                data["fi_name"] = [
                    "This field is required."
                ]
            if not rit_id:
                data["rit_name"] = [
                    "This field is required."
                ]
            if not base_date:
                data["base_date"] = [
                    "This field is required."
                ]
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
