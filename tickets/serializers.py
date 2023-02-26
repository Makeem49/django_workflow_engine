from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["title", "body","publish", "date_created", "date_updated"]


class TicketDecideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["title", "body","publish", "status","date_created", "date_updated"]