from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import (TicketSerializer, 
                        TicketDecideSerializer,
                        TicketDetailsSerializer, 
                        TicketOwnerSerializer)
from .models import Ticket
from .utils import get_list
from .exceptions import CannotPerformOperation, MissingData
from departments.models import Department
from users.models import User
from .permissions import (
            IsAuthorizeUserPermissionOnly, 
            IsAuthorizeToRaiseIssue, 
            IsAuthor,
            IsPermittedToMakeDecision)
from .tasks import send_email
from .utils import get_alert



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
        return get_list(self)



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
        instance = self.get_object()
        level = self.request.user.level.name.strip().lower()
        user_department = instance.user.department.name.strip()
        department = Department.objects.filter(name=user_department).first()
        obj = self.get_object()
        if obj.publish:
            """If the ticket has been publish, avoid ability to update the ticket"""
            raise CannotPerformOperation()
        instance = serializer.save()
        print(instance.publish, type(instance.publish), "+++++++++++++++++++++")
        get_alert(level, instance, User, department)
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
    # permission_classes = [IsAuthorizeUserPermissionOnly]
    permission_classes = [IsAuthorizeUserPermissionOnly, IsPermittedToMakeDecision]


    def perform_update(self, serializer):
        print(self.request.data)
        instance = self.get_object()
        user_department = instance.user.department.name.strip()
        department = Department.objects.filter(name=user_department).first()
        user_email = instance.user.email
        current_user = self.request.user
        status = self.request.data['status'].strip().lower()
        new_body = ''
        new_title = ''
        if self.request.data.get('action.publish') :
            new_title = self.request.data['action.title']
            new_body = self.request.data['action.body']
            publish = self.request.data.get('action.publish')
        
        if self.request.data.get('action'):
            excalate_data = self.request.data.get('action')
            new_title = excalate_data.get('title')
            new_body = excalate_data.get('body')
            publish = excalate_data.get('publish')

        message = f"""
                Hello {instance.user.first_name}, there is an update on your ticket, kindly check it out.\n 

                Ticket information:

                Ticket ID : {instance.ticket_id}
                Created at: {instance.date_updated}
                Created by: {instance.user.first_name} {instance.user.last_name}
                Department: {instance.user.department.name}
                Emaployee tag: {instance.user.employee_identification_tag}
                Employee level: {instance.user.level.name.capitalize()}

                Thanks. 
            """

        if status == 'approve' or status == 'deny' or status=='pending': 
            send_email.delay(instance.title, message, current_user.email, user_email)

        elif status == 'excalated':
            """If the ticket is excalated, create a new ticket, and notify the superior person in charge of the excalated issue."""
            ticket = None
            if new_title and new_body:
                ticket = Ticket.objects.create(user=current_user, department=instance.department, title=new_title, body=new_body, publish=publish)
                # if instance.tickets:
                #     instance.tickets.children.add(ticket)
                # else:
                #     instance.children.add(ticket)
                instance.children.add(ticket)
                    # send_email(instance.title, message, current_user.email, user_email)
            else:
                raise MissingData()



        instance = serializer.save()

        return Response(serializer.data)


class OwnerTicketView(generics.ListAPIView):
    """This endpoint will list all the user ticket either created or non created."""

    queryset = Ticket.objects.all()
    serializer_class = TicketOwnerSerializer
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