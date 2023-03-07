from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Level
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from departments.models import Department

class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")


    def test_create_superuser(self):
            User = get_user_model()
            admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
            self.assertEqual(admin_user.email, "super@user.com")
            self.assertTrue(admin_user.is_active)
            self.assertTrue(admin_user.is_staff)
            self.assertTrue(admin_user.is_superuser)
            try:
                # username is None for the AbstractUser option
                # username does not exist for the AbstractBaseUser option
                self.assertIsNone(admin_user.username)
            except AttributeError:
                pass
            with self.assertRaises(ValueError):
                User.objects.create_superuser(
                    email="super@user.com", password="foo", is_superuser=False)
                

class UserTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            phone="555-555-5555",
            position="Manager"
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), "John Doe test@example.com")

    def test_employee_identification_tag(self):
        self.assertEqual(self.user.employee_identification_tag, "John-555-555-5555-Doe")

    def test_employee_identification_tag_unique(self):
        with self.assertRaises(Exception):
            User = get_user_model()
            user2 = User.objects.create(
                email="test2@example.com",
                first_name="Jane",
                last_name="Doe",
                phone="555-555-5555",
                position="Developer",
                assword='password'
            )

    def test_generate_identification(self):
        self.assertEqual(self.user.generate_identication, "John-555-555-5555-Doe")

    def test_username_field(self):
        self.assertEqual(self.user.get_username(), "test@example.com")

    def test_required_fields(self):
        self.assertEqual(self.user.REQUIRED_FIELDS, ['first_name', 'last_name'])

    def test_save_employee_identification_tag(self):
        User = get_user_model()
        user2 = User.objects.create(
            email="test2@example.com",
            first_name="Jane",
            last_name="Doe",
            phone="555-555-5558",
            position="Cyber officer",
            password='password'
        )
        self.assertEqual(user2.employee_identification_tag, "Jane-555-555-5558-Doe")



class LevelModelTest(TestCase):
    def setUp(self):
        self.level = Level.objects.create(name='Manager')

    def test_string_representation(self):
        self.assertEqual(str(self.level), self.level.name)


class EmployeeCommon(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='adminpass',
            department =  Department.objects.create(name='Administrative department'),
            level = Level.objects.create(name='Head of department')
        )

        self.token = Token.objects.create(user=self.admin_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)



class EmployeeDetailViewTest(EmployeeCommon, APITestCase):
    def setUp(self):
        super().setUp()
        self.employee = get_user_model().objects.create_user(
            email='employee@test.com',
            password='testpass',
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            position='analyst'
        )
        self.department = Department.objects.create(name='IT')
        self.employee.department = self.department
        self.employee.level = Level.objects.create(name='supervisor')
        self.employee.save()


    def test_retrieve_employee_detail_with_valid_permission(self):
        """Test that an admin user with valid permissions can retrieve an employee detail"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('employee-detail', kwargs={'pk': self.employee.pk})
        response = self.client.get(url)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_employee_detail_without_valid_permission(self):
        """Test that an admin user without valid permissions cannot retrieve an employee detail"""
        self.employee.level = Level.objects.create(name='analyst')
        self.employee.save()

        url = reverse('employee-detail', kwargs={'pk': self.employee.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EmployeeListViewTest(EmployeeCommon, APITestCase):
    def test_retrieve_employee_list_with_valid_permission(self):
        """Test that an admin user with valid permission can retrieve all employee list"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('employee-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_employee_list_with_no_valid_permission(self):
        """Test that an admin user without valid permission can retrieve all employee list"""
        url = reverse('employee-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
class EmloyeeDeleteViewTest(EmployeeCommon, APITestCase):
    def setUp(self):
        super().setUp()
        self.employee = get_user_model().objects.create_user(
            email='employee@test.com',
            password='testpass',
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            position='analyst'
        )
        self.department = Department.objects.create(name='IT')
        self.employee.department = self.department
        self.employee.level = Level.objects.create(name='supervisor')
        self.employee.save()

    
    def test_delete_employee_detail_with_valid_permission(self):
        """Test that an admin user with valid permissions can delete an employee detail"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('employee-deactivate', kwargs={'pk': self.employee.pk})
        response = self.client.delete(url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)