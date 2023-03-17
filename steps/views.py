from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .models import Step
from stages.models import Stage
from process.models import Process
from .serializers import StepSerializer
from rest_framework.response import Response

class StepCreateView(generics.CreateAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    lookup_field='pk'

    def create(self, request, *args, **kwargs):
        stage_id = self.kwargs['stage_id']
        process_id = self.kwargs['process_id']
        process = get_object_or_404(Process, pk=process_id)
        stage = get_object_or_404(Stage, pk=stage_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(stage=stage)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StepListView(generics.ListAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer 
    lookup_field='pk'

    def get_queryset(self):
        stage_id = self.kwargs['stage_id']
        process_id = self.kwargs['process_id']
        process = get_object_or_404(Process, pk=process_id)
        stage = get_object_or_404(Stage, pk=stage_id)
        queryset = Step.objects.filter(stage=stage)
        return queryset


class StepDetailView(generics.RetrieveAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer 
    lookup_field='pk'

    def get_object(self):
        stage_id = self.kwargs['stage_id']
        process_id = self.kwargs['process_id']
        process = get_object_or_404(Process, pk=process_id)
        stage = get_object_or_404(Stage, pk=stage_id)
        obj = Step.objects.filter(stage=stage).first()
        return obj


class StepUpdateView(generics.UpdateAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    lookup_field='pk'


class StepDeactivateView(generics.DestroyAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    lookup_field='pk'