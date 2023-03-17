from rest_framework import generics
from .models import Process
from .serializers import ProcessSerializer, ProcessDetailSerializer

class ProcessCreateView(generics.CreateAPIView):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    lookup_field='pk'


class ProcessListView(generics.ListAPIView):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer 
    lookup_field='pk'


class ProcessDetailView(generics.RetrieveAPIView):
    queryset = Process.objects.all()
    serializer_class = ProcessDetailSerializer 
    lookup_field='pk'


class ProcessUpdateView(generics.UpdateAPIView):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    lookup_field='pk'


class ProcessDeactivateView(generics.DestroyAPIView):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    lookup_field='pk'