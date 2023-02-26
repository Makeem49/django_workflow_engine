from rest_framework import generics, status, permissions, authentication
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError

from .models import User
from .serializers import UserSerializer




class EmployeeListCreateView(generics.ListCreateAPIView):
    """View handling creating a new employee"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]


class EmployeeDetailView(generics.RetrieveAPIView):
    """View handling retrieve an employee""" 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        # Get all User objects and their associated Employee objects
        queryset = User.objects.select_related('employee')

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        print(context)
        return context


class EmployeeDeactivateView(generics.DestroyAPIView):
    """View to disable a company employee from accessing the platform"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def delete(self, *args, **kwargs):
        instance = self.get_object()
        print('user',instance.is_active)
        try:
            super().delete(self, *args, **kwargs)
        except ProtectedError as e:
            instance.is_active = False
            obj = {}
            instance.save()
            return Response(obj, status=status.HTTP_204_NO_CONTENT)

