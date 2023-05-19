from django.shortcuts import get_object_or_404
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from uf.models import ValuesUF
from uf.serializers import ValuesUFSerializer


class ValuesUFViewSet(GenericViewSet):
    serializer_class = ValuesUFSerializer
    queryset = ValuesUF.objects.all()
    permission_classes = [DjangoObjectPermissions]

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, value_date):
        value_uf = get_object_or_404(self.queryset, date=value_date.date())
        serializer = ValuesUFSerializer(value_uf)
        return Response(serializer.data)
