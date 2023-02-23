from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    """Department serializer"""
    url = serializers.HyperlinkedIdentityField(
            view_name='department-detail',
            lookup_field='pk',
            read_only=True
    )
    
    class Meta:
        model = Department
        fields = ['name','url',
                'active', 'date_created', "date_update"]
