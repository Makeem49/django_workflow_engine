from rest_framework import serializers
from .models import Department

from users.models import User
from users.serializers import UserSerializer
from tickets.models import Ticket


class DepartmentSerializer(serializers.ModelSerializer):
    """Department serializer"""
    url = serializers.HyperlinkedIdentityField(
            view_name='department-detail',
            lookup_field='pk',
            read_only=True
    )

    employees = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Department
        fields = ['name','url',
                'active', 'date_created', "date_update", 'employees']
    

    def get_employees(self, obj):
        users = User.objects.filter(department=obj).count()
        return users
	

class DepartmentDetailSerializer(serializers.ModelSerializer):
    """Department serializer"""
    url = serializers.HyperlinkedIdentityField(
            view_name='department-detail',
            lookup_field='pk',
            read_only=True
    )

    employees = serializers.SerializerMethodField(read_only=True)
    number_of_ticket = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Department
        fields = ['name','url',
                'active', 'date_created', "date_update", 'number_of_ticket','employees']

    def get_employees(self, obj):
        users = User.objects.filter(department=obj)
        users = UserSerializer(users, many=True).data
        return users

    def get_number_of_ticket(self, obj):
        tickets_num = Ticket.objects.filter(department=obj).count()
        return tickets_num

    

