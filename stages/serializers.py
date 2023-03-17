from rest_framework import serializers
from .models import Stage
from rest_framework.reverse import reverse
from steps.serializers import StepSerializer


class StageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Stage
        fields = ['url', 'name']

    def get_url(self, obj):
        request = self.context.get('request')
        url = reverse('stage-detail', args=[obj.process.id, obj.id], request=request)
        return url


    
class StageDetailSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Stage
        fields = ['actions']


    def get_actions(self, obj):
        actions = obj.action_set.all()
        request = self.context.get('request')
        actions_data = StepSerializer(actions, many=True, context={'request': request}).data
        return actions_data
    