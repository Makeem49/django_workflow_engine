from uuid import uuid4

from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.
class Ticket(models.Model):
    """
    Ticket model to create a ticket for the root user who open the ticket
    """
    STATUS = [
        ('Pending', 'Pending'),
        ('Approve', 'Approve'),
        ('Deny', 'Deny'),
        ('Excalated', 'Excalated')
    ]

    CHOICE = [
        ('False', False),
        ('True', True)
    ]

    ticket_id = models.UUIDField(default=uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=timezone.now)
    status = models.CharField(max_length=10, default='pending', choices=(STATUS))
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False, related_name='user_tickets')
    tickets = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='children')
    publish = models.BooleanField(default=False, choices=CHOICE)
    department = models.ForeignKey('departments.Department', null=False, blank=True, on_delete=models.PROTECT)


    class Meta:
        ordering  = ['-date_updated']

    def __str__(self) -> str:
        return f"{self.title} ------> {self.status}"

