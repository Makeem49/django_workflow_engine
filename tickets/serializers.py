from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='ticket-details',
            lookup_field='pk',
            read_only=True
    )

    class Meta:
        model = Ticket
        fields = ["url","title", "body","publish", "date_created", "date_updated"]



    
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

    class Meta:
        model = Ticket
        fields = ["title", "body","publish", "status","date_created", "date_updated", "action"]

    def create(self, validated_data):
        print('created')
        return super().create(validated_data)


    def update(self, instance, validated_data):
        print('saved')
        user = self.context['request'].user
        new_ticket_data = validated_data.get('action')
        if instance.status.strip().lower() == 'excalated':
            print('excaled pppppppp')
            if new_ticket_data['title'] and new_ticket_data['body']:
                ticket = Ticket.objects.create(user=user, department=instance.department, **new_ticket_data)
                instance.tickets = ticket
                print(instance.tickets)
        return super().update(instance, validated_data)