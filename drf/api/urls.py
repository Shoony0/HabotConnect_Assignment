from django.urls import path
from api import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('employees/<uuid:id>/', views.EmployeesView.as_view(), name='employees'),
    path('employees/', views.EmployeesView.as_view(), name='employees'),
]
