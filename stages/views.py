from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Stage
from .serializers import StageSerializer, StageDetailSerializer
from process.models import Process

class StageCreateView(generics.CreateAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    lookup_field='pk'


    def create(self, request, *args, **kwargs):
        process_id = self.kwargs['process_id']
        process = get_object_or_404(Process, pk=process_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(process=process)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StageListView(generics.ListAPIView):
    serializer_class = StageSerializer

    def get_queryset(self):
        process_id = self.kwargs['process_id']
        process = get_object_or_404(Process, pk=process_id)
        queryset = Stage.objects.filter(process=process)
        return queryset
    
    def get_serializer_context(self):
        process_id = self.kwargs['process_id']
        return {
            'request': self.request,
            'process_name': self.format_kwarg,
            'view': self,
            'process_name' : process_id
        }


class StageDetailView(generics.RetrieveAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageDetailSerializer
    lookup_url_kwarg = ['process_id']

    def get_object(self):
        process_id = self.kwargs['process_id']
        stage_id = self.kwargs['pk']
        process = get_object_or_404(Process, pk=process_id)
        stage = get_object_or_404(Stage, pk=stage_id)
        print(stage)
        return stage
    



class StageUpdateView(generics.UpdateAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    lookup_field='pk'

    def get_object(self):
        process_id = self.kwargs['process_id']
        stage_id = self.kwargs['pk']
        process = get_object_or_404(Process, pk=process_id)
        stage = get_object_or_404(Stage, pk=stage_id)
        return stage


class StageDeactivateView(generics.DestroyAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    lookup_field='pk'

    def get_object(self):
        process_id = self.kwargs['process_id']
        stage_id = self.kwargs['pk']
        process = get_object_or_404(Process, pk=process_id)
        stage = get_object_or_404(Stage, pk=stage_id)
        return stage