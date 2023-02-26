from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from uuid import uuid4

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):

    CHOICE = [
        (True, 'True'),
        (False, 'False')
    ]

    username = None
    email = models.EmailField(_("email address"), unique=True, null=False)
    is_active = models.BooleanField(choices=CHOICE, default=True)
    phone = models.CharField(max_length=11, null=False, unique=True)
    employee_identification_tag = models.CharField(max_length=50, null=False, blank=False, unique=True)
    position = models.CharField(max_length=20, null=False, blank=False)
    department = models.ForeignKey("departments.Department", on_delete=models.PROTECT, null=True)
    level = models.ForeignKey("Level", on_delete=models.PROTECT, null=True, blank=True)
    

    @property
    def generate_identication(self):
        unique_id = f"{self.first_name}-{self.phone}-{self.last_name}"
        return unique_id
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"

    def save(self, *args, **kwargs):
        self.employee_identification_tag = self.generate_identication
        return super(User, self).save(*args, **kwargs)



class Level(models.Model):
    """Role model"""

    name = models.CharField(max_length=20, null=False, unique=True)
    date_created = models.DateField(auto_now_add=timezone.now) 

    def __str__(self) -> str:
        return f"{self.name}"
    

