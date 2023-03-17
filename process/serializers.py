from rest_framework import serializers
from .models import Process
from stage.serializers import StageSerializer


class ProcessSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='process-detail',
        lookup_field = 'pk',
        read_only=True
    )

    class Meta:
        model = Process
        # fields = ['url', 'name']
        fields = ['url', 'name']

    
class ProcessDetailSerializer(serializers.ModelSerializer):
    stages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Process
        fields = ['stages']

    def get_stages(self, obj):
        stages = obj.stage_set.all()
        request = self.context.get('request') 
        stages = StageSerializer(stages, many=True, context={'request': request}).data
        return stages