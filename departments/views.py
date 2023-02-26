from rest_framework import generics, status
from rest_framework.response import Response

from django.db.models.deletion import ProtectedError

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentListCreateView(generics.ListCreateAPIView):
    """View to create and list department view"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        qs = Department.objects.filter(active=True)
        return qs


class DepartmentDetail(generics.RetrieveAPIView):
    """View to view the detail of a department"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'pk'


class DepartmentDeactivateView(generics.DestroyAPIView):
    """View to deactivate a particular department"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'pk'

    def delete(self, *args, **kwargs):
        instance = self.get_object()
        try:
            super().delete(self, *args, **kwargs)
        except ProtectedError as e:
            instance.active = False
            obj = {}
            instance.save()
            return Response(obj, status=status.HTTP_204_NO_CONTENT)