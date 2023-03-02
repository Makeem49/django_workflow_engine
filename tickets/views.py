from rest_framework import generics, permissions
from django.db.models.signals import post_save

from .serializers import TicketSerializer, TicketDecideSerializer, TicketDetailsSerializer
from .models import Ticket
from .exceptions import CannotPerformOperation
from .permissions import (
            IsAuthorizeUserPermissionOnly, 
            IsAuthorizeToRaiseIssue, 
            IsAuthor,
            IsPermittedToMakeDecision)



class TicketCreateView(generics.CreateAPIView):
    """This view allow authenticated user and user that are fully integrated into the company to create a ticket.
    
    *Requirement*
    1. Must be authenticated
    2. Must have a level and belong to a department.
    
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsAuthorizeToRaiseIssue]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, department=self.request.user.department)


class TicketListView(generics.ListAPIView):
    """This view allow user from supervisor level and above to access this endpoint to check the numbe rof tickets that has been raised.

    *Requiremnt *
    1. Must be authenticated.
    2. MUst have a level above analyst to access the endpoint.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsAuthorizeUserPermissionOnly]

    def get_queryset(self):
        """The custom query set only allow user of a particular level
        to see ticket issues raise by user lower in level than them.
        """
        user = self.request.user
        level = user.level.name.strip().lower()
        department = user.department.name

        qs = Ticket.objects.filter(publish=True).filter(tickets=None)
        # if user.is_superuser:
        #     return qs 

        if level == 'supervisor':
            """Supervisor only see tickets open by the analyst which has been published in the same department.
            """
            qs = Ticket.objects.filter(user__level__name__iexact='Analyst')\
                        .filter(department__name__iexact=department)\
                            .filter(publish=True).filter(tickets=None)

        elif level == 'head of department':
            """Head of department only see tickets opened by the department supervisor he is heading.
               """
            qs = Ticket.objects.filter(user__level__name__iexact='supervisor')\
                    .filter(department__name__iexact=department)\
                        .filter(publish=True)

        elif level == 'cto/cfo':
            """The cto/cfo only see the ticket open by any head of department in the company.
            """
            qs = Ticket.objects.filter(user__level__name__iexact='head of department')\
                .filter(publish=True)

        elif level == 'president':
            """The president only see tickets open by either the cto/cfo of the comapny.
            """
            qs = Ticket.objects.filter(user__level__name__iexact='cto/cfo')\
                .filter(publish=True)

        elif level == 'ceo':
            """The ceo can only see list of tickets of teh company presidents."""
            qs = Ticket.objects.filter(user__level__name__iexact='president')\
                .filter(publish=True)
        return qs



class TicketDetailView(generics.RetrieveAPIView):
    """View to view the detail of a department
    
    *Requirement*
    1. Must be authenticated.
    2. Must have meet all the permission requirement.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketDetailsSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsPermittedToMakeDecision]


class TicketUpdateView(generics.RetrieveUpdateAPIView):
    """
    Endpoint where the owner of the ticket can update the ticket 
    if it has not been publish.
    *Requirement*
    1. Must be authenticated
    2. Must be the owner of the ticket
    """
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
    """
    Endpoint to allow user to delete their draft ticket.
    *Requirement*
    1. Must be authenticated
    2. Must be the owner
    3. Must not have been published.
    """
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
    """
    Endpoint where further decision can be made on a ticket by the superior.

    *Requirements*
    1. Must have a level above analyst
    2. Must meet the requirement of approving, deny or escalating a ticket
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketDecideSerializer
    permission_classes = [IsAuthorizeUserPermissionOnly, IsPermittedToMakeDecision]


    def perform_update(self, serializer):
        current = self.request.user 
        post_save.send(sender=Ticket, instance=serializer.instance, created=False, user=current, request=self.request, dispatch_uid='my_unique_identifier')
        return super().perform_update(serializer)


class OwnerTicketView(generics.ListAPIView):
    """This endpoint will list all the user ticket either created or non created."""

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthor]

    
    def get_queryset(self):
        """Get lis of the owner tickets."""
        tickets = self.request.GET.get('publish')
        publish_ticket = self.request.GET.get('publish')
        user = self.request.user
        qs = Ticket.objects.filter(user=user)
        if tickets:
            qs = Ticket.objects.filter(user=user, publish=publish_ticket)
        return qs