from rest_framework import serializers
from .models import User
from departments.models import Department
from tickets.models import Ticket


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
            'password', 'is_active', 'phone', 'position', "department", "level"]

    def create(self, validated_data):
        instance = User.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        department = rep.get('department')
        dept_name = Department.objects.filter(id=department).first()
        rep['department'] = dept_name.name 
        rep['level'] = instance.level.name
        rep['tickets'] = Ticket.objects.filter(user=instance).count()
        return rep
