from api.models import Employee
from rest_framework import serializers
from django.contrib.auth.models import User
from api import utils

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('name', 'email', 'department', 'role', )
    
    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        employee = Employee(**validated_data)
        employee.save()
        return employee
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department'] = utils.get_department_name_by_id(instance.department)
        representation['role'] = utils.get_role_name_by_id(instance.role)
        return representation

class GetEmployeeSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('id', 'name', 'email', 'department', 'role', 'date_joined',)
    

    def get_department(self, instance):
        return utils.get_department_name_by_id(instance.department)
    
    def get_role(self, instance):
        return utils.get_role_name_by_id(instance.role)
    
class UpdateEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('name', 'email', 'department', 'role',)  # adjust fields as needed


