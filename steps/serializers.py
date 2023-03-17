from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Step


class StepSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Step
        fields = ['url', 'name', 'stage']

    def get_url(self, obj):
        request = self.context.get('request')
        # print(obj.stage.process.id, '============')
        # print(obj.stage.id, '*********')
        url = reverse('action-detail', args=[obj.stage.process.id, obj.stage.id, obj.id], request=request)
        return url

    
# class ActionDetailSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Step
#         fields = ['actions']

#     def get_actions(self, obj):
#         stages = obj.stage_set.all()
#         request = self.context.get('request') 
#         stages = ActionSerializer(stages, many=True, context={'request': request}).data
#         return stages
    
    