import json
import random
from api.models import DEPARTMENT_CHOISE, ROLE_CHOISE, Employee
from rest_framework.test import APITestCase, APIRequestFactory
from api import utils, views
from django.urls import reverse

# Create your tests here.


class EmployeesTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.employee_view = views.EmployeesView.as_view()
        self.employee_uri = reverse("api:employees")

        # Ceate a new user
        self.register_user_view = views.RegisterView.as_view()
        self.register_user_uri = reverse("api:register")
        request_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "test_user",
            "email": "test_user@example.com",
            "password": "abc123"
        }

        request = self.factory.post(
            self.register_user_uri,
            data=json.dumps(request_data),
            content_type="application/json",
        )
        response = self.register_user_view(request)
        self.assertEqual(response.status_code, 201)

        # Login a register user to get token
        self.login_user_view = views.LoginView.as_view()
        self.login_user_uri = reverse("api:login")
        request_data = {
            "username": "test_user",
            "password": "abc123"
        }

        request = self.factory.post(
            self.login_user_uri,
            data=json.dumps(request_data),
            content_type="application/json",
        )
        response = self.login_user_view(request)
        self.assertEqual(response.status_code, 200)
        self.token = f'Token {response.data["token"]}'

    def test_create_employee(self):
        """
        Creating employee
        DEPARTMENT_CHOISE = (
            (0, "HR"),
            (1, "Engineering"),
            (2, "Sales"),
        )

        ROLE_CHOISE = (
            (0, "Manager"),
            (1, "Developer"),
            (2, "Analyst"),
        )
        """
        # creating 25 Employee
        for i in range(25):
            request_data = {
                "name": f"Employee {i+1}",
                "email": f"employee.{i+1}@example.com",
                "department": random.choice([0, 1, 2]),
                "role": random.choice([0, 1, 2]),
            }
            request = self.factory.post(
                self.employee_uri,
                data=json.dumps(request_data),
                content_type="application/json",
                HTTP_AUTHORIZATION=self.token
            )
            response = self.employee_view(request)
            self.assertEqual(response.status_code, 201)

        
    
    def test_view_employee(self):
        self.test_create_employee()

        request = self.factory.get(
            self.employee_uri,
            content_type="application/json",
            HTTP_AUTHORIZATION=self.token
        )
        response = self.employee_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 25)
        return response.data
    
    def test_get_employee_by_id(self):
        all_employees = self.test_view_employee()
        employee_id = all_employees[0]["id"]
        employee_uri = reverse("api:employees", kwargs={
            "id": employee_id
        })
        request = self.factory.get(
            employee_uri,
            content_type="application/json",
            HTTP_AUTHORIZATION=self.token
        )
        response = self.employee_view(request, id=employee_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.data["id"], employee_id)

    def test_filter_employee_by_department(self):
        self.test_create_employee()

        new_employee_uri=f"{self.employee_uri}?department=HR"
        request = self.factory.get(
            new_employee_uri,
            content_type="application/json",
            HTTP_AUTHORIZATION=self.token
        )
        response = self.employee_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["department"], "HR")

    def test_filter_employee_by_role(self):
        self.test_create_employee()

        new_employee_uri=f"{self.employee_uri}?role=Developer"
        request = self.factory.get(
            new_employee_uri,
            content_type="application/json",
            HTTP_AUTHORIZATION=self.token
        )
        response = self.employee_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["role"], "Developer")

    def test_filter_employee_by_page(self):
        self.test_create_employee()

        new_employee_uri=f"{self.employee_uri}?page=2"
        request = self.factory.get(
            new_employee_uri,
            content_type="application/json",
            HTTP_AUTHORIZATION=self.token
        )
        response = self.employee_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

    
    def test_update_employee_details(self):
        """
        Update employee Details
        DEPARTMENT_CHOISE = (
            (0, "HR"),
            (1, "Engineering"),
            (2, "Sales"),
        )

        ROLE_CHOISE = (
            (0, "Manager"),
            (1, "Developer"),
            (2, "Analyst"),
        )
        """

        all_employees = self.test_view_employee()
        employee_id = all_employees[0]["id"]
        employee_uri = reverse("api:employees", kwargs={
            "id": employee_id
        })
        request_data = {
            "name": "Employee One Update",
            "email": "employee.one.update@example.com",
            "department": 1,
            "role": 2,
        }
        request = self.factory.put(
            employee_uri,
            data=json.dumps(request_data),
            content_type="application/json",
            HTTP_AUTHORIZATION=self.token
        )
        response = self.employee_view(request, id=employee_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        employee = Employee.objects.get(id=employee_id)
        response_data = response.data
        self.assertEqual(employee.name, response_data["name"])
        self.assertEqual(employee.email, response_data["email"])
        self.assertEqual(utils.get_department_name_by_id(employee.department), response_data["department"])
        self.assertEqual(utils.get_role_name_by_id(employee.role), response_data["role"])
    
    def test_delete_employee(self):
        """
        delete employee
        """

        all_employees = self.test_view_employee()
        employee_id = all_employees[0]["id"]
        employee_uri = reverse("api:employees", kwargs={
            "id": employee_id
        })
        request = self.factory.delete(
            employee_uri,
            content_type="application/json",
            HTTP_AUTHORIZATION=self.token
        )
        response = self.employee_view(request, id=employee_id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Employee.objects.filter(id=employee_id).exists())

