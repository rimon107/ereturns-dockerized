from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ereturns.institutes.api.serializers import FinancialInstituteSerializer
from ereturns.institutes.models import FinancialInstitute


class FinancialInstituteViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FinancialInstituteSerializer
    queryset = FinancialInstitute.objects.all()
    lookup_field = "id"
