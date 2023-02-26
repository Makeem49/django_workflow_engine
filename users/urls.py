from django.urls import path, include
from users import views

urlpatterns = [
    path('employee/', views.EmployeeListCreateView.as_view(), name='employee-create'),
    path('employee/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/<int:pk>/deactivate/', views.EmployeeDeactivateView.as_view(), name='employee-deactivate'),
]