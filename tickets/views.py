from rest_framework import generics, permissions, authentication


from .serializers import TicketSerializer, TicketDecideSerializer
from .models import Ticket
from .exceptions import CannotPerformOperation
from .permissions import IsAuthorizeUserPermissionOnly
from tokens.authentications import TokenAuthentication


# Create your views here.
class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
    # authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request.user.department)
        serializer.save(user=self.request.user, department=self.request.user.department)


class TicketListView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
    # authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Ticket.objects.filter(publish=True)
        return qs


class TicketDetailView(generics.RetrieveAPIView):
    """View to view the detail of a department"""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
    # authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class TicketUpdateView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
    # authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.publish:
            """If the ticket has been publish, avoid ability to update the ticket"""
            raise CannotPerformOperation()
        return super().perform_update(serializer)


class TicketDeleteView(generics.DestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
    # authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.publish:
            """If ticket has been publish, avoid ability to delete the ticket"""
            raise CannotPerformOperation()
        if self.request.user == instance.user:
            return super().perform_destroy(instance)


class TicketDecisionView(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketDecideSerializer
    # authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [ permissions.IsAdminUser, IsAuthorizeUserPermissionOnly]


    def perform_update(self, serializer):
        obj = self.request.user.level 
        print(obj)
        return super().perform_update(serializer)


class OwnerTicketView(generics.ListAPIView):
    """This endpoint will list all the user ticket either created or non created."""

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        tickets = self.request.GET.get('publish')
        publish_ticket = self.request.GET.get('publish')
        user = self.request.user
        qs = Ticket.objects.filter(user=user)
        if tickets:
            qs = Ticket.objects.filter(user=user, publish=publish_ticket)
        return qs