from rest_framework import generics


from .serializers import TicketSerializer
from .models import Ticket


# Create your views here.
class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketListView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Ticket.objects.filter(publish=True)
        return qs


class TicketDetail(generics.RetrieveAPIView):
    """View to view the detail of a department"""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'