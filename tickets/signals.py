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

    level = instance.user.level.name.lower().strip()
    user_department = instance.user.department.name.strip()
    department = Department.objects.filter(name=user_department).first()
    all_levels = ['analyst', 'supervisor', 'cto/cfo', 'head of department', 'president', 'ceo']
    if created:
        # print('create')
        # print(instance.publish, type(instance.publish), '************************')
        if level in all_levels and (instance.publish==True or instance.publish=='True'):
            """Send alert if the user condition if true."""
            # print('sending message alert')
            get_alert(level, instance, User, department)