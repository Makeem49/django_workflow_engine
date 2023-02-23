from django.db import models
from django.utils import timezone

# Create your models here.
class Department(models.Model):
    """Department model"""
    CHOICE = [
        (True, 'True'),
        (False, 'False')
    ]
    name = models.CharField(max_length=30, null=False, blank=False)
    active = models.BooleanField(default=True, choices=CHOICE, null=False)
    supervisor = models.OneToOneField('users.User', null=True, blank=True, on_delete=models.PROTECT,related_name='department_supervisor')
    head_of_department = models.OneToOneField('users.User', null=True, blank=True, on_delete=models.PROTECT, related_name='department_head')
    date_update = models.DateTimeField(auto_now=timezone.now)
    date_created = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{self.name}"


    def __str__(self):
        return f"{self.name}"

