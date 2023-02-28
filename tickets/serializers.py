from rest_framework import serializers
from .models import Ticket

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

    class Meta:
        model = Ticket
        fields = ["title", "body","publish", "status","date_created", "date_updated","tickets"]

    def get_tickets(self, obj):
        tickets = obj.children.all()
        request = self.context.get('request')
        tickets = TicketSerializer(tickets, many=True, context={'request': request}).data
        return tickets

    
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

    class Meta:
        model = Ticket
        fields = ["title", "body","publish", "status","date_created", "date_updated","tickets", "action"]

    def get_tickets(self, obj):
        tickets = obj.children.all()
        request = self.context.get('request')
        tickets = TicketSerializer(tickets, many=True, context={'request': request}).data
        return tickets


    def create(self, validated_data):
        return super().create(validated_data)


    def update(self, instance, validated_data):
        user = self.context['request'].user
        new_ticket_data = validated_data.get('action')
        if validated_data.get('status').lower().strip() == 'excalated':
            if new_ticket_data['title'] and new_ticket_data['body']:
                ticket = Ticket.objects.create(user=user, department=instance.department, **new_ticket_data)
                instance.children.add(ticket)
                instance.save()
        return super().update(instance, validated_data)