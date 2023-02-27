from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ticket
from users.models import User
from departments.models import Department
from .utils import get_alert

@receiver(post_save, sender=Ticket)
def create_ticket(sender, instance, created, **kwargs):
    """Help create a ticket profile when the a new issue is created
    * Todo 
    1. Notify the appropriate user when a new ticket is raised
    2. Send an email and sms message to the appropriate user base on role and department 
    """
    if created:

        level = instance.user.level.name.lower().strip()

        user_department = instance.user.department.name.strip()
        print(user_department, '*******')

        department = Department.objects.filter(name=user_department).first()

        all_levels = ['analyst', 'supervisor', 'cto/cfo', 'head of department', 'president', 'ceo']
        if level in all_levels:
            """Send alert if the user condition if true."""
            get_alert(level, instance, User, department)


@receiver(post_save, sender=Ticket)
def save_ticket(sender, instance, **kwargs):
    """Notify the high authority of the change in file."""

    level = instance.user.level.name.lower()

    department = instance.department

    """The logic"""

    # if superior is accessing the ticket and is updating it for either accept or deny
    # notify the owner of the ticket, else if escalate, notify the superior in the department 

    # if the user is the one updating is ticket, don't notify anybody 

    