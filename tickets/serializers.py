from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["title", "body","publish", "date_created", "date_updated"]
