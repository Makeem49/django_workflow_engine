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
        url = reverse('action-detail', args=[obj.stage.process.id, obj.stage.id, obj.id], request=request)
        return url