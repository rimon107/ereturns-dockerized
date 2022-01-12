from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from ereturns.institutes.api.serializers import FinancialInstituteSerializer, BranchSerializer
from ereturns.institutes.models import FinancialInstitute, Branch
from django.db.models import Q

User = get_user_model()

class FinancialInstituteViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny, )
    serializer_class = FinancialInstituteSerializer
    queryset = FinancialInstitute.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(~Q(name="Bangladesh Bank"))

    @action(detail=False, methods=["GET"])
    def branch(self, request):
        fi_id = self.request.GET.get('fi_id')
        queryset = Branch.objects.filter(financial_institute_id=fi_id).exclude(name__iexact="Head Office")
        serializer = BranchSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="user-count")
    def user_count(self, request):
        fi_id = self.request.GET.get('fi_id')
        queryset = User.objects.filter(financial_institute_id=fi_id)
        branch_id = self.request.GET.get('branch_id')
        group = Group.objects.filter(name="Bank HO end user")[0]
        ho_users = queryset.filter(groups__id=group.id).count()
        data = {
            "ho_users": ho_users
        }
        if branch_id:
            group = Group.objects.filter(name="Bank Branch end user")[0]
            branch_users = queryset.filter(branch__id=branch_id, groups__id=group.id).count()
            print(branch_users)
            data["branch_users"] = branch_users

        return Response(status=status.HTTP_200_OK, data=data)
