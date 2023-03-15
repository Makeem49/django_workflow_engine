from tickets.tasks import send_email
from .models import Ticket
from .exceptions import MissingData
from users.models import User
from .constants import (
        analyst,
        supervisor,
        ceo,
        hod,
        president,
        cto
)


def message_template(user, instance):
    """Message template"""
    message = f"""
                Hello {user}, a ticket an been raised, kindly check it out.\n 

                Ticket information:

                Ticket ID : {instance.ticket_id}
                Created at: {instance.date_updated}
                Created by: {instance.user.first_name} {instance.user.last_name}
                Department: {instance.user.department.name}
                Emaployee tag: {instance.user.employee_identification_tag}
                Employee level: {instance.user.level.name.capitalize()}

                Thanks. 
            """

    return message


def get_alert(level, instance, model, department):
    """
    levl: user level 
    instance : the save instance ticket
    model : User model for getting a particuler user
    department: department to get he department superior email 
    email: The ticket opener emal address 
    """
    if department and instance.publish: 

        if level == analyst.name:
            """Get the supervisor email attach to the department."""
            supervisor_email = department.supervisor.email
            message = message_template(department.supervisor.first_name, instance)
            """
            * Todo: Send email notifying the supervisor of the department an alert 
            """
            send_email.delay(instance.title, message, instance.user.email, supervisor_email)


        elif level == supervisor.name:
            """Get the head of department email."""
            head_of_department_email = department.head_of_department.email
            message = message_template(department.head_of_department.first_name, instance)

            """
            * Todo: Send email notifying the head of department an alert
            """
            send_email.delay(instance.title, message, instance.user.email, head_of_department_email)

        elif level == hod.name:
            """Get the company cto/cfo email"""
            cto_or_cfo = model.objects.filter(level__name='CTO/CFO').first()
            cto_or_cfo_email = cto_or_cfo.email
            message = message_template(cto_or_cfo.first_name, instance)

            """
            * Todo: Send email to the cto/cfo of the company an alert 
            """
            send_email.delay(instance.title, message, instance.user.email, cto_or_cfo_email)

        elif level == cto.name:
            """Get the company president email"""
            president = model.objects.filter(level__name = 'President').first()
            president_email = president.email
            message = message_template(president.first_name, instance)

            """
            * Todo: Send email to the company president
            """
            send_email.delay(instance.title, message, instance.user.email, president_email)

        elif level == president.name:
            """Get the CEO email"""
            ceo = model.objects.filter(level__name = 'CEO').first()
            ceo_email = ceo.email 
            message = message_template(ceo.first_name, instance)

            """
            * Todo: Send email to the CEO of the president
            """
            send_email.delay(instance.title, message, instance.user.email, ceo_email)

    else:
        print('Not sending email')

def get_list(self):
    user = self.request.user
    level = user.level.name.strip().lower()
    department = user.department.name

    qs = Ticket.objects.filter(publish=True).filter(tickets=None)
    # if user.is_superuser:
    #     return qs 

    if level == supervisor.name:
        """Supervisor only see tickets open by the analyst which has been published in the same department.
        """
        qs = Ticket.objects.filter(user__level__name__iexact='Analyst')\
                    .filter(department__name__iexact=department)\
                        .filter(publish=True).filter(tickets=None)

    elif level == hod.name:
        """Head of department only see tickets opened by the department supervisor he is heading.
            """
        qs = Ticket.objects.filter(user__level__name__iexact='supervisor')\
                .filter(department__name__iexact=department)\
                    .filter(publish=True)

    elif level == cto.name:
        """The cto/cfo only see the ticket open by any head of department in the company.
        """
        qs = Ticket.objects.filter(user__level__name__iexact='head of department')\
            .filter(publish=True)

    elif level == president.name:
        """The president only see tickets open by either the cto/cfo of the comapny.
        """
        qs = Ticket.objects.filter(user__level__name__iexact='cto/cfo')\
            .filter(publish=True)

    elif level == ceo.name:
        """The ceo can only see list of tickets of teh company presidents."""
        qs = Ticket.objects.filter(user__level__name__iexact='president')\
            .filter(publish=True)
    return qs


 
