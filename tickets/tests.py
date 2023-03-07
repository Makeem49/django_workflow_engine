from django.test import TestCase
from departments.models import Department
from .models import Ticket
from users.models import User, Level
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, Level
from tickets.models import Ticket
from departments.models import Department
from django.contrib.auth import get_user_model


# Create your tests here.
class TicketModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='IT')
        self.level = Level.objects.create(name='Manager')
        self.user = User.objects.create(
            email='test@test.com',
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            position='Software Engineer',
            department=self.department,
            level = self.level
        )
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            body='This is a test ticket.',
            user=self.user,
            department=self.department
        )

    def test_string_representation(self):
        self.assertEqual(str(self.ticket), f"{self.ticket.title} ------> {self.ticket.status}")

    def test_status_choices(self):
        choices = [status[0] for status in Ticket.STATUS]
        self.assertListEqual(choices, ['Pending', 'Approve', 'Deny', 'Excalated'])

    def test_publish_choices(self):
        choices = [publish[0] for publish in Ticket.CHOICE]
        self.assertListEqual(choices, ['False', 'True'])

    def test_child_tickets_are_created(self):
        child_ticket = Ticket.objects.create(
            title='Child Ticket',
            body='This is a child ticket.',
            user=self.user,
            department=self.department,
            tickets=self.ticket
        )
        self.assertIn(child_ticket, self.ticket.children.all())




User = get_user_model()

class EmployeeListCreateViewTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
            first_name="Admin",
            last_name="User",
            phone="1234567890",
            position="admin",
            department=Department.objects.create(name="Administrative Department"),
            level=Level.objects.create(name="Head of department")
        )

    def test_admin_can_create_employee(self):
        """
        Ensure that an admin user can create a new employee via the EmployeeListCreateView.
        """
        self.client.force_authenticate(user=self.admin_user)

        data = {
            "email": "newemployee@example.com",
            "password": "newemployeepassword",
            "first_name": "New",
            "last_name": "Employee",
            "phone": "0987654324",
            "position": "analyst",
            "department": Department.objects.create(name="Finance Department").id,
            "level": Level.objects.create(name="Analyst").id
        }

        response = self.client.post(reverse("employee-list-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

        new_employee = User.objects.get(email="newemployee@example.com")
        self.assertEqual(new_employee.first_name, "New")
        self.assertEqual(new_employee.last_name, "Employee")
        self.assertEqual(new_employee.phone, "0987654324")
        self.assertEqual(new_employee.position, "analyst")
        self.assertEqual(new_employee.department.name, "Finance Department")
        self.assertEqual(new_employee.level.name, "Analyst")

    def test_analyst_cannot_create_employee(self):
        """
        Ensure that an analyst user cannot create a new employee via the EmployeeListCreateView.
        """
        analyst_user = User.objects.create_user(
            email="analyst@example.com",
            password="analystpassword",
            first_name="Analyst",
            last_name="User",
            phone="1234567899",
            position="analyst",
            department=Department.objects.create(name="Finance Department"),
            level=Level.objects.create(name="cto/cfo")
        )

        self.client.force_authenticate(user=analyst_user)

        data = {
            "email": "newemployee@example.com",
            "password": "newemployeepassword",
            "first_name": "New",
            "last_name": "Employee",
            "phone": "0987654324",
            "position": "supervisor",
            "department": Department.objects.create(name="Finance Department").id,
            "level": Level.objects.create(name="Analyst").id
        }

        response = self.client.post(reverse("employee-list-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)
