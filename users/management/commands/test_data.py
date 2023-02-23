from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import User, Department, Employee

class Command(BaseCommand):
    help = 'Add test data into the model for testing.'

    # def add_arguments(self, parser):
    #     parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        user = User.objects.filter(email='admin@gmail.com')
        if not user:
            user = User.objects.create_superuser(email='admin@gmail.com', password='password', first_name='Admin', last_name='Panel')
        else:
            user = User.objects.create_user(email='John@gmail.com', password='password', first_name='John', last_name='Doe')

        department = Department.objects.filter(name='IT')
        if not department:
            department = Department.objects.create(name='IT')
        else:
            department = Department.objects.create(name='Accounting')

        employee = Employee.objects.filter(phone='12345678901')

        if not employee:
            employee = Employee(phone='12345678901', position='Accountant')
            employee.department_id = department.id
            employee.user = user
            employee.save()
        