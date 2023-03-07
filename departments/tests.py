from django.test import TestCase
from rest_framework.authtoken.models import Token
from .models import Department
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from departments.models import Department
from users.models import Level, User

# Create your tests here.
class DepartmentModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='IT')

    def test_string_representation(self):
        self.assertEqual(str(self.department), self.department.name)

    def test_active_choices(self):
        choices = [active[0] for active in Department.CHOICE]
        self.assertListEqual(choices, [True, False])



class DepartmentCommon(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='adminpass',
            department =  Department.objects.create(name='Administrative department'),
            level = Level.objects.create(name='Head of department')
        )

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


        self.token = Token.objects.create(user=self.admin_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)



class DepartmentDetailViewTest(DepartmentCommon, APITestCase):
    def setUp(self):
        super().setUp()
        self.department = Department.objects.create(name='IT')
        self.department.save()


    def test_retrieve_department_detail_with_valid_permission(self):
        """Test that an admin user with valid permissions can retrieve a department detail"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('department-detail', kwargs={'pk': self.department.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_department_detail_without_valid_permission(self):
        """Test that an admin user without valid permissions cannot retrieve an department detail"""

        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.force_authenticate(user=self.user)

        url = reverse('department-detail', kwargs={'pk': self.department.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DepartmentListViewTest(DepartmentCommon, APITestCase):
    def test_retrieve_department_list_with_valid_permission(self):
        """Test that an admin user with valid permission can retrieve all department list"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('department-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_department_list_with_no_valid_permission(self):
        """Test that an admin user without valid permission can retrieve all department list"""
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.force_authenticate(user=self.user)

        url = reverse('employee-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
class DepartmentDeactivateViewTest(DepartmentCommon, APITestCase):
    
    def test_deactivate_department_with_valid_permission(self):
        """Test that an admin user with valid permissions can deactivate a department detail"""
        self.client.force_authenticate(user=self.admin_user)
        print(Department.objects.all())
        url = reverse('employee-deactivate', kwargs={'pk': self.department.pk})
        response = self.client.delete(url)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)