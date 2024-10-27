import uuid
from django.db import models
from django.contrib.auth.models import User


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


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    department = models.SmallIntegerField(choices=DEPARTMENT_CHOISE, default=0)
    role = models.SmallIntegerField(choices=ROLE_CHOISE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)