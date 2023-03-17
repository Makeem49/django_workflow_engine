from django.db import models
from django.utils import timezone

# Create your models here.
class Process(models.Model):
    """Model for creating process"""
    name = models.CharField(max_length=100, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField( auto_now=True)


    def __str__(self) -> str:
        return f"{self.name}"