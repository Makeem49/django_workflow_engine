from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError

from .models import User
from .serializers import UserSerializer
# from departments.permissions import IsAdminApproveUserOnly



class EmployeeListCreateView(generics.ListCreateAPIView):
    """View handling creating a new employee"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAdminUser, IsAdminApproveUserOnly]


class EmployeeDetailView(generics.RetrieveAPIView):
    """View handling retrieve an employee""" 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAdminUser, IsAdminApproveUserOnly]



class EmployeeDeactivateView(generics.DestroyAPIView):
    """View to disable a company employee from accessing the platform"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAdminUser, IsAdminApproveUserOnly]

    def delete(self, *args, **kwargs):
        instance = self.get_object()
        try:
            super().delete(self, *args, **kwargs)
            obj = {}
            return Response(obj, status=status.HTTP_204_NO_CONTENT)
        except ProtectedError as e:
            instance.is_active = False
            obj = {}
            instance.save()
            return Response(obj, status=status.HTTP_204_NO_CONTENT)

