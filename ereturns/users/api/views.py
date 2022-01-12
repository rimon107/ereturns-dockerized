from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.settings import api_settings

from .serializers import UserSerializer, UserPasswordUpdateSerializer
from django.utils.translation import gettext_lazy as _
from ...institutes.models import FinancialInstitute, Branch, FinancialInstituteType

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        group_id = self.request.user.groups.all()[0].id
        if group_id==1:
            list_queryset = self.queryset
        else:
            fi_id = self.request.user.financial_institute.id
            list_queryset = self.queryset.filter(
                groups__id=group_id, financial_institute__id=fi_id)
        queryset = self.filter_queryset(list_queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["GET"])
    def members(self, request):
        active = User.objects.filter(is_active=True).count()
        inactive = User.objects.filter(is_active=False).count()
        online = User.objects.filter(status=1).count()
        data = {
            "active": active,
            "inactive": inactive,
            "online": online,
        }
        return Response(status=status.HTTP_200_OK, data=data)

class UserPasswordChangeViewSet(GenericViewSet):
    serializer_class = UserPasswordUpdateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    @action(detail=False, methods=["PATCH"], url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        user = self.request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if not user.check_password(current_password):
            raise ValidationError(
                ({'wrong_password': _('Your existing password was entered incorrectly. Please try again.')})
            )
        if new_password != confirm_password:
            raise ValidationError({'password_mismatch': _("The new and confirm password didn't match.")})

        if current_password == new_password:
            raise ValidationError({'password_same': _("The current and new password must be different.")})

        user.set_password(new_password)
        user.save()
        data = {
            "success": "Password successfully changed.",
        }
        return Response(status=status.HTTP_200_OK, data=data)


class UserRegistrationViewSet(GenericViewSet):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    queryset = User.objects.select_related("financial_institute_type", "financial_institute", "branch")
    lookup_field = "id"

    @action(detail=False, methods=["POST"], url_path="add")
    def add(self, request, *args, **kwargs):
        report_type = request.data.get("report_type")
        group_name = None
        if report_type:
            if report_type == "br_end_usr":
                group_name = "Bank Branch end user"
            elif report_type == "ho_end_usr":
                group_name = "Bank HO end user"
            else:
                data = {
                    "report_type": ["Report Type is not valid"]
                }
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
        group = Group.objects.filter(name=group_name)[0]
        fi_id = int(request.data.get("financial_institute_id"))
        branch = None
        branch_id = None
        if group_name == "Bank Branch end user":
            branch_id = int(request.data.get("branch_id"))
            try:
                branch = Branch.objects.get(id=branch_id)
            except Branch.DoesNotExist:
                data = {
                    "branch": ["branch is not valid"]
                }
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
        elif group_name == "Bank HO end user":
            branch = Branch.objects.filter(financial_institute_id=fi_id, name__iexact="Head Office")
            if branch.exists():
                branch = branch.first()
            else:
                data = {
                    "branch": ["branch is not valid"]
                }
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
        last_user_code = None
        if group_name=="Bank HO end user":
            last_user = User.objects.filter(financial_institute_id=fi_id, groups__id=group.id)
            if last_user.exists():
                print(last_user)
                last_user_code = last_user.last().user_code
            else:
                last_user_code = branch.code + "-" + "00"
        elif group_name=="Bank Branch end user":
            last_user = User.objects.filter(financial_institute_id=fi_id, branch_id=branch_id)
            if last_user.exists():
                last_user_code = last_user.last().user_code
            else:
                last_user_code = branch.code + "-" + "00"
        code = int(last_user_code.split("-")[-1]) + 1
        code = code if len(str(code)) > 1 else "0"+str(code)
        username = branch.code + "-" + code
        financial_institute_type_id = request.data.get("financial_institute_type_id", None),
        financial_institute_id = int(request.data.get("financial_institute_id")),
        fi_type = None
        try:
            fi_type = FinancialInstituteType.objects.get(id=financial_institute_type_id[0])
        except FinancialInstituteType.DoesNotExist:
            data = {
                "financial institute type": ["financial institute type is not valid"]
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
        fi = None
        try:
            fi = FinancialInstitute.objects.get(id=financial_institute_id[0])
        except FinancialInstitute.DoesNotExist:
            data = {
                "financial institute": ["financial institute is not valid"]
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
        data = {
            "name": request.data.get("employee_name"),
            "username": username,
            "user_code": username,
            'financial_institute_type': fi_type.id,
            'financial_institute': fi.id,
            'branch': branch.id,
            'password': request.data.get("password"),
            'designation': request.data.get("designation"),
            'department': request.data.get("department"),
            'email': request.data.get("email"),
            'mobile': request.data.get("mobile"),
            'phone': request.data.get("phone"),
            "status": "Offline",
            "is_active": False,
            "groups": [group.id]
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @action(detail=False, methods=["GET"], url_path="check-limit")
    def check_user_limit(self, request):
        fi_id = self.request.GET.get('fi_id')
        branch_id = self.request.GET.get('branch_id')
        if not branch_id:
            count = self.queryset.filter(groups__id=3, financial_institute__id=fi_id).count()
            data = {
                "msg": "HO Branch User Limit Exceeded!" if count>4 else "HO Branch User can be created",
                "status": False if count>4 else True
            }
        else:
            count = self.queryset.filter(groups__id=4,
                                            financial_institute__id=fi_id,
                                            branch__id=branch_id).count()
            data = {
                "msg": "Branch User Limit Exceeded!" if count>1 else "Branch User can be created",
                "status": False if count>1 else True
            }
        return Response(status=status.HTTP_200_OK, data=data)
