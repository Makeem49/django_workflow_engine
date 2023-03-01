from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ticket
from users.models import User
from departments.models import Department
from .utils import get_alert, message_template
from .tasks import send_mail

@receiver(post_save, sender=Ticket, dispatch_uid='my_unique_identifier')
def create_ticket(sender, instance, created, **kwargs):
    """Help create a ticket profile when the a new issue is created
    * Todo 
    1. Notify the appropriate user when a new ticket is raised
    2. Send an email and sms message to the appropriate user base on role and department 
    """

    level = instance.user.level.name.lower().strip()
    user_department = instance.user.department.name.strip()
    department = Department.objects.filter(name=user_department).first()
    all_levels = ['analyst', 'supervisor', 'cto/cfo', 'head of department', 'president', 'ceo']
    if created:
        if level in all_levels:
            """Send alert if the user condition if true."""
            get_alert(level, instance, User, department)

    else:

        status = instance.status.lower().strip()

        if department and instance.publish and status == 'excalated': 

            get_alert(level, instance, User, department)

        elif status == 'approve' or status == 'deny':
            user_email = instance.user.email
            ticket_title = f"Ticket update on {instance.title}"
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
            curret_request = kwargs.get('request')
            if curret_request:
                print('send update email')
                send_mail(ticket_title, message, curret_request.user.email, user_email)