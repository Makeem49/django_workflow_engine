from rest_framework import serializers
from .models import Ticket
from rest_framework.reverse import reverse

class TicketSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='ticket-details',
            lookup_field='pk',
            read_only=True
    )

    department = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ["url","title", "body","publish", "status","department", "date_created", "date_updated"]


    def get_department(self, obj):
        department = obj.department.name
        return department

    def get_status(self, obj):
        return obj.status


class TicketDetailsSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField(read_only=True)
    decide_url = serializers.SerializerMethodField(read_only=True)
    user_tag = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Ticket
        fields = ["decide_url","title", "body","publish", "user_tag","status","date_created", "date_updated","tickets"]

    def get_tickets(self, obj):
        tickets = obj.children.all()
        request = self.context.get('request') 
        tickets = TicketSerializer(tickets, many=True, context={'request': request}).data
        return tickets

    def get_user_tag(self, obj):
        return obj.user.employee_identification_tag
    
    def get_decide_url(self, obj):
        return reverse('ticket-decide', args=[obj.id], request=self.context.get('request'))

    
    

    
class TicketActionSerializer(serializers.Serializer):
    CHOICE = [
        (False, 'False'),
        (True, 'True')
    ]

    title = serializers.CharField(required=False, max_length=100)
    body = serializers.CharField(required=False, max_length=500)
    publish = serializers.ChoiceField(default='False', choices=(CHOICE))


class TicketDecideSerializer(serializers.ModelSerializer):
    action = TicketActionSerializer(required=False)
    tickets = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    body = serializers.SerializerMethodField(read_only=True)
    publish = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = ["title", "body","publish", "status","date_created", "date_updated","tickets", "action"]

    def get_tickets(self, obj):
        tickets = obj.children.all()
        request = self.context.get('request')
        tickets = TicketSerializer(tickets, many=True, context={'request': request}).data
        return tickets
    
    def get_title(self, obj):
        return obj.title
    
    def get_body(self, obj):
        return obj.body
    
    def get_publish(self, obj):
        return obj.publish


    def create(self, validated_data):
        return super().create(validated_data)


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

class TicketOwnerSerializer(serializers.ModelSerializer):
    update_url = serializers.SerializerMethodField(read_only=True)

    department = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ["update_url","title", "body","publish", "status","department", "date_created", "date_updated"]


    def get_department(self, obj):
        department = obj.department.name
        return department

    def get_status(self, obj):
        return obj.status
    
    def get_update_url(self, obj):
        return  reverse('ticket-update', args=[obj.id], request=self.context.get('request'))