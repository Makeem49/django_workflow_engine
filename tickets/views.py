from rest_framework import generics, permissions, authentication
from django.db.models.signals import post_save

from .serializers import TicketSerializer, TicketDecideSerializer, TicketDetailsSerializer
from .models import Ticket
from .exceptions import CannotPerformOperation
from .permissions import (
            IsAuthorizeUserPermissionOnly, 
            IsAuthorizeToRaiseIssue, 
            IsAuthor,
            IsPermittedToMakeDecision)


# Create your views here.
class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsAuthorizeToRaiseIssue]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, department=self.request.user.department)


class TicketListView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsAuthorizeUserPermissionOnly]

    def get_queryset(self):
        user = self.request.user
        level = user.level.name.strip().lower()
        department = user.department.name

        qs = Ticket.objects.filter(publish=True).filter(tickets=None)
        if user.is_superuser:       
            return qs 

        if level == 'supervisor':
            qs = Ticket.objects.filter(user__level__name__iexact='Analyst')\
                        .filter(department__name__iexact=department)\
                            .filter(publish=True).filter(tickets=None)

        elif level == 'head of department':
            qs = Ticket.objects.filter(user__level__name__iexact='supervisor')\
                    .filter(department__name__iexact=department)\
                        .filter(publish=True).filter(tickets=None)

        elif level == 'cto/cfo':
            qs = Ticket.objects.filter(user__level__name__iexact='head of department')\
                .filter(publish=True).filter(tickets=None)

        elif level == 'president':
            qs = Ticket.objects.filter(user__level__name__iexact='cto/cfo')\
                .filter(publish=True).filter(tickets=None)

        elif level == 'ceo':
            qs = Ticket.objects.filter(user__level__name__iexact='president')\
                .filter(publish=True).filter(tickets=None)
        return qs



class TicketDetailView(generics.RetrieveAPIView):
    """View to view the detail of a department"""
    queryset = Ticket.objects.all()
    serializer_class = TicketDetailsSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsPermittedToMakeDecision]


class TicketUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsAuthor]


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
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def perform_destroy(self, instance):
        user = self.request.user

        if instance.user != user:
            raise CannotPerformOperation(detail='Operation cannot be perform', code=423)

        if instance.publish:
            """If ticket has been publish, avoid ability to delete the ticket"""
            raise CannotPerformOperation()
        if self.request.user == instance.user:
            return super().perform_destroy(instance)


class TicketDecisionView(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketDecideSerializer
    permission_classes = [IsAuthorizeUserPermissionOnly, IsPermittedToMakeDecision]


    def perform_update(self, serializer):
        current = self.request.user 
        print(current.email)
        post_save.send(sender=Ticket, instance=serializer.instance, created=False, user=current, request=self.request, dispatch_uid='my_unique_identifier')
        return super().perform_update(serializer)


class OwnerTicketView(generics.ListAPIView):
    """This endpoint will list all the user ticket either created or non created."""

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthor]

    
    def get_queryset(self):
        tickets = self.request.GET.get('publish')
        publish_ticket = self.request.GET.get('publish')
        user = self.request.user
        qs = Ticket.objects.filter(user=user)
        if tickets:
            qs = Ticket.objects.filter(user=user, publish=publish_ticket)
        return qs