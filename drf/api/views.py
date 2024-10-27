from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from api import serializers, utils
from api.models import Employee
from django.contrib.auth.models import User
from rest_framework import status
from django.core.paginator import Paginator

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer
    permission_classes = (AllowAny,)

class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid Credentials"}, status=400)

    
class EmployeesView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = serializers.CreateEmployeeSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        department = request.GET.get("department", None)
        role = request.GET.get("role", None)
        page = request.GET.get("page", None)

        if id is None:
            many = True
            employees = Employee.objects.all().order_by("date_joined")
        else:
            many = False
            employees = Employee.objects.filter(id=id)
            if employees.exists():
                employees=employees.get()
            else:
                return Response(
                    {
                    "message": "Invalid employee ID."
                    }, status=status.HTTP_404_NOT_FOUND
                )
        
        if department is not None:
            department_id = utils.get_department_id_by_name(department)
            employees = employees.filter(department=department_id).order_by("date_joined")
        
        if role is not None:
            role_id = utils.get_role_id_by_name(role)
            employees = employees.filter(role=role_id).order_by("date_joined")
        
        if page is not None:
            # creating a paginator object
            p = Paginator(employees, 10)
            try:
                employees = p.get_page(number=int(page))  # returns the desired page object
            except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
                employees = p.page(1)
            except EmptyPage:
                # if page is empty then return last page
                employees = p.page(p.num_pages)
        

        serializer = serializers.GetEmployeeSerializer(employees, many=many)
        return Response(serializer.data)
    
    def put(self, request, id):
        employee = Employee.objects.filter(id=id)
        if employee.exists():
            employee=employee.get()
        else:
            return Response(
                {
                "message": "Invalid employee ID."
                }, status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.UpdateEmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer_data = serializer.data

            serializer_data["department"] = utils.get_department_name_by_id(serializer_data["department"])
            serializer_data["role"] = utils.get_role_name_by_id(serializer_data["role"])
    
            return Response(serializer_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            employee = Employee.objects.get(id=id)
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({"message": "Invalid employee ID."}, status=status.HTTP_404_NOT_FOUND)
    
